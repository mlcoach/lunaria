import datetime
from functools import wraps
from uuid import UUID
import uuid
import fastapi
from fastapi.responses import JSONResponse
from fastapi import Depends, status
from dto.login.user_login_request_dto import UserLoginRequestDTO
from dto.register.user_register_request_dto import UserRegisterRequestDTO
from models.role_model import UserRoles
from models.user_login_model import UserLoginModel
from models.user_model import UserModel
from services.user_service import UserService
from repos.user_repo import UserRepository
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
import jwt
import os
import hashlib
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

user_service:UserService = UserService(user_repository=UserRepository(session=Cluster().connect('users')))
connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)

sync_table(UserModel)
sync_table(UserLoginModel)
sync_table(UserRoles)



secret_key = os.environ.get('SECRET_KEY')

app = fastapi.FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def root():
    return {"message": "Service is running..."}


def auth_required():
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            request = kwargs['request']
            allowed_roles = kwargs['allowed_roles']
            if 'Authorization' not in request.headers:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                    "message": "Missing token"
                })
            token = request.headers['Authorization'].replace('Bearer ', '')
            try:
                user = jwt.decode(token, str(secret_key), algorithms=["HS256"])
                id = uuid.UUID(user['uid'])
                user = user_service.get_user_by_id(UserModel, id)
                if user.is_active:
                    user_role = user_service.get_user_role_by_id(user.role)
                    if user_role.name in allowed_roles:
                       return await func(*args, **kwargs)
                    else:
                        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                            "message": "User is not authorized"
                        })
                else:
                    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                        "message": "User is not active"
                    })
            except Exception as e:
                print(e)
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                    "message": "Invalid token"
                })
        return wrapped
    return wrapper


@app.get("/users", status_code=200)
@auth_required()
@limiter.limit("10/minute")
async def get_users(request: fastapi.Request, allowed_roles: list[str] = ['admin']):
    try:
        queries = user_service.get_users(UserModel)
        users = []
        for user in queries:
            role = user_service.get_user_role_by_id(user.role).name
            users.append({
                "uid": str(user.uid),
                "username": user.username,
                "email": user.email,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "role": role,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
            })
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "users": users
        })
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "message": str(e)
        })


@app.get("/users/{user_id}", status_code=200)
@limiter.limit("10/minute")
@auth_required()
async def get_user_by_id(user_id: UUID ,request: fastapi.Request,allowed_roles: list[str] = ['admin', 'user']):

    try:
        user = user_service.get_user_by_id(UserModel, user_id)
        role = user_service.get_user_role_by_id(user.role).name
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "uid": str(user.uid),
            "username": user.username,
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "role": role,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
        })
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "message": str(e)
        })



@app.post("/auth/login", status_code=200)
@limiter.limit("5/minute")
async def login(request: fastapi.Request, userDTO: UserLoginRequestDTO):
    try:
        if(userDTO.username == None and userDTO.email != None):
            user = user_service.get_user_by_email(UserModel, userDTO.email)
        elif(userDTO.username != None and userDTO.email == None):
            user = user_service.get_user_by_username(UserModel, userDTO.username)
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                "message": "Invalid request"
            })
        if validatePassword(user.uid, userDTO.password):
            role = user_service.get_user_role_by_id(user.role)
            payload = {
                "username": user.username,
                "uid": str(user.uid),
                "email": user.email,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "role": role.name,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
            }
            token = jwt.encode(payload, str(secret_key), algorithm="HS256")
            return JSONResponse(status_code=status.HTTP_200_OK, content={
                "token": token,
                "expires": str(datetime.datetime.utcnow() + datetime.timedelta(days=10)),
            })
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                "message": "Invalid password"
            })
    except Exception as e:
       return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                "message": str(e)
            })

@app.post("/auth/register", status_code=201)
@limiter.limit("5/minute")
async def register(request: fastapi.Request, userDTO:UserRegisterRequestDTO):
    try: 
        user_service.create_user(userDTO)  
    except Exception as e:
        if "Record already exists" in str(e):
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
                                "message": str(e)
                            })
        else:
           raise e
    try:
        user = user_service.get_user_by_username(UserModel, userDTO.username)
        admin_role = user_service.get_user_role_by_name("admin")
        user_role = user_service.get_user_role_by_name("user")
        payload = {
            "username": user.username,
            "uid": str(user.uid),
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "role": admin_role.name if user.is_superuser == True else user_role.name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
        }
        token = jwt.encode(payload, str(secret_key), algorithm="HS256")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "token": token,
            "expires": str(datetime.datetime.utcnow() + datetime.timedelta(days=10)),
        })
    except Exception as e:
            raise Exception(e)

@app.post("/auth/verify", status_code=200)
@limiter.limit("5/minute")
async def verify(request: fastapi.Request, token: str):
    try:
        jwt.decode(token, str(secret_key), algorithms=["HS256"])
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "Valid token"
        })
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
            "message": "Invalid token"
        })

@app.put("/auth/update/user-model", status_code=200)
@limiter.limit("50/minute")
async def update(request: fastapi.Request, update):
    token = request.headers['Authorization'].replace('Bearer ', '')
    try:
        decoded_token = jwt.decode(token, str(secret_key), algorithms=["HS256"])
        user = user_service.get_user_by_id(UserModel,  UUID(decoded_token['uid']))
        user_service.update_user(update, UserModel, user.uid)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
            "message": "Invalid token"
        })


def validatePassword(user_id, password):
    user = user_service.get_user_by_id(UserLoginModel, user_id)
    if user.passwordHash == hashPassword(password + user.passwordSalt):
        return True
    else:
        return False

def hashPassword(password):
    return hashlib.sha256((password).encode('utf-8')).hexdigest()

