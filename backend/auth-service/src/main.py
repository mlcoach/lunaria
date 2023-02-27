import fastapi
from dto.login.user_login_request_dto import UserLoginRequestDTO
from services.user_service import UserService
from repos.user_repo import UserRepository
from cassandra.cluster import Cluster
# from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
import jwt
import os


user_service:UserService = UserService(user_repository=UserRepository(session=Cluster().connect('users')))
connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)


app = fastapi.FastAPI()

@app.post("/auth/login", status_code=200)
async def login(userDTO: UserLoginRequestDTO):
    #todo: validate user
    user = user_service.get_user(userDTO.username)
    #todo: return jwt token
    token = jwt.encode({**user}, os.getenv('secret_key'), algorithm="HS256")
    return {

    }

@app.post("/auth/register", status_code=201)
async def register(userDTO):
    #todo: validate user
    #todo: create user
    #todo: return jwt token
    pass

@app.post("/auth/verify", status_code=200)
async def verify(token:str):
    #todo: validate token
    #todo: return token or success
    pass

@app.post("/auth/logout", status_code=200)
async def logout(token:str):
    #todo: validate token
    #todo: delete token
    #todo: return success
    pass