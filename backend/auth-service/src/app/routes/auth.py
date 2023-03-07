import dataclasses
import datetime
from uuid import UUID
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
import jwt

from ..dependencies import limiter, user_service, validatePassword, secret_key, templates
from models.user_model import UserModel
from dto.login.user_login_request_dto import UserLoginRequestDTO
from models.user_login_model import UserLoginModel
from dto.register.user_register_request_dto import UserRegisterRequestDTO
from api.google_api.email_verification import EmailVerification

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, userDTO: UserLoginRequestDTO):
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
            payload = dataclasses.asdict(user_service.mapToUserResponseModel(user))
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

@router.post("/register", status_code=201)
@limiter.limit("5/minute")
async def register(request: Request, userDTO: UserRegisterRequestDTO):
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
        verifiable_user = user_service.get_user_by_id(UserLoginModel, user.uid)
        email = EmailVerification(user.email,verifiable_user)
        payload = {
            "uid": str(user.uid)
        }
        email.send()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=payload)

    except Exception as e:
            raise Exception(e)    

@router.post("/verify", status_code=200)
@limiter.limit("5/minute")
async def verify(request: Request, token: str):
    try:
        jwt.decode(token, str(secret_key), algorithms=["HS256"])
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "Valid token"
        })
    
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
            "message": "Invalid token"
        })

@router.get("/verify/{token}", status_code=200)
@limiter.limit("50/minute")
async def verify(request: Request, token: str):
    try:
        decoded_token = jwt.decode(token, str(secret_key), algorithms=["HS256"])
        user = user_service.get_user_by_id(UserLoginModel, UUID(decoded_token['user_id']))
        if datetime.datetime.utcnow() > datetime.datetime.fromtimestamp(decoded_token['exp']):
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                "message": "Expired token"
            })
        if user.confirmationToken == token:
            user_service.update_user(UserLoginModel, user.uid,  {"confirmationToken": None,
                                                                      "confirmationTokenExpiration": None,
                                                                      "emailVerified": True
                                                                      })
            return templates.TemplateResponse("verification.html", {"request": request})
        elif user.confirmationToken == None:
            return templates.TemplateResponse("already_verified.html", {"request": request})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                "message": "Invalid token"
            })
    except Exception as e:
        if "Signature has expired" in str(e):
            return templates.TemplateResponse("expired.html", {"request": request})
        raise Exception(e)
        

