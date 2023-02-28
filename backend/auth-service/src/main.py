import datetime
from uuid import UUID
import fastapi
from fastapi.responses import JSONResponse
from fastapi import Depends, status
from dto.login.user_login_request_dto import UserLoginRequestDTO
from dto.register.user_register_request_dto import UserRegisterRequestDTO
from models.user_login_model import UserLoginModel
from models.user_model import UserModel
from services.user_service import UserService
from repos.user_repo import UserRepository
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
# from cassandra.cqlengine.management import sync_table
import jwt
import os
import hashlib
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

user_service:UserService = UserService(user_repository=UserRepository(session=Cluster().connect('users')))
connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)

# sync_table(UserModel)
# sync_table(UserLoginModel)

secret_key = os.environ.get('SECRET_KEY')

app = fastapi.FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def root():
    return {"message": "Service is running..."}


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
            payload = {
                "username": user.username,
                "uid": str(user.uid),
                "email": user.email,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "role": str(user.role),
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
    try:
        user = user_service.get_user_by_username(UserModel, userDTO.username)
        payload = {
            "username": user.username,
            "uid": str(user.uid),
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "role": str(user.role),
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
        user = user_service.get_user_by_argument(UserModel,  UUID(decoded_token['uid']))
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