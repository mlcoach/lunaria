from datetime import datetime, timedelta
from pydantic.dataclasses import dataclass
from typing import Optional
from models.user_model import UserModel
from dto.register.user_register_request_dto import UserRegisterRequestDTO
from utilities.model_mapper import map_schema
from models.user_login_model import UserLoginModel
register = UserRegisterRequestDTO(username="test", password="test", email="test", firstName="test", lastName="test")
user = map_schema(register, UserModel)
user_login = map_schema(register, UserLoginModel)
print(user_login.passwordHash)