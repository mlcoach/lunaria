import fastapi
from dto.login.user_login_request_dto import UserLoginDTO
from services.user_service import UserService


def main():
    
    user_service:UserService = UserService()

    app = fastapi.FastAPI()

    @app.post("/auth/login", status_code=200)
    async def login(userDTO:UserLoginDTO):
        #todo: validate user
        #todo: return jwt token
        pass
    
    @app.post("/auth/register", status_code=201)
    async def register(userDTO:UserLoginDTO):
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

    
if __name__ == "__main__":
    main()