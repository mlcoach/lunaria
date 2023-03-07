from uuid import UUID
from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from models.user_model import UserModel
from models.user_login_model import UserLoginModel
from dto.register.user_register_request_dto import UserRegisterRequestDTO
from api.google_api.email_verification import EmailVerification

from models.error_model import ErrorModel
from constants.error_enum import ErrorEnum

from ..dependencies import auth_required, limiter, user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code=200)
@auth_required(allowed_roles=['admin'])
@limiter.limit("10/minute")
async def get_users(request: Request):
    try:
        users = user_service.get_users()
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "users": users
        })
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "message": str(e)
        })


@router.get("/{uid}", status_code=200)
@limiter.limit("10/minute")
@auth_required(allowed_roles=['admin', 'user'])
async def get_user(uid: UUID, request: Request):
    try:
        user = user_service.get_user_by_id(UserModel, uid)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            user
        })
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "message": str(e)
        })


@router.post("/", status_code=201)
@limiter.limit("10/minute")
async def create_user(request: Request, userDTO: UserRegisterRequestDTO):
    try: 
        user_service.create_user(userDTO)  
    except ErrorModel as e:
        if e.status_code == ErrorEnum.USER_ALREADY_EXISTS.value:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
                                "message": str(e)
                            })
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                                "message": str(e)
                            })
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
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "message": str(e)
        })
            


@router.put("/{uid}", status_code=200)
@limiter.limit("10/minute")
@auth_required(allowed_roles=['admin', 'user'])
async def update_user(uid: UUID, request: Request, userDTO):
    try:
        user_service.update_user(uid, userDTO)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"uid": uid})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content={
            "message": "Invalid token"
        })


@router.delete("/{uid}", status_code=200)
@limiter.limit("50/minute")
@auth_required(allowed_roles=['admin'])
async def update(request: Request, uid: UUID):
    try:
        user_service.delete_user(uid)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"uid": uid})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
            "message": "Invalid token"
        })
