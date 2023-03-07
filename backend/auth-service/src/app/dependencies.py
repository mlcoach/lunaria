from functools import wraps
from hashlib import sha256
import os
import uuid
from slowapi import Limiter
from slowapi.util import get_remote_address
from cassandra.cluster import Cluster
import jwt
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from models.user_login_model import UserLoginModel
from repos.user_repo import UserRepository
from services.user_service import UserService
from models.user_model import UserModel

limiter = Limiter(key_func=get_remote_address)

user_service = None

user_service = user_service if user_service != None else UserService(
    user_repository=UserRepository(session=Cluster().connect('users')))

secret_key = os.environ.get('SECRET_KEY')

templates = Jinja2Templates(directory="templates")


def validatePassword(user_id, password):
    user = user_service.get_user_by_id(UserLoginModel, user_id)
    if user.passwordHash == hashPassword(password + user.passwordSalt):
        return True
    else:
        return False


def hashPassword(password):
    return sha256((password).encode('utf-8')).hexdigest()


def auth_required(allowed_roles: list[str]):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            request = kwargs['request']
            if 'Authorization' not in request.headers:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                    "message": "Missing token"
                })
            try:
                token = request.headers['Authorization'].replace('Bearer ', '')
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
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                    "message": "Invalid token"
                })
        return wrapped
    return wrapper
