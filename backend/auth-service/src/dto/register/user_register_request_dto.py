
from dataclasses import dataclass
from typing import Optional
from pydantic import  Field

@dataclass
class UserRegisterRequestDTO():
    username: str = Field(..., min_length=3, max_length=15)
    password: str = Field(..., min_length=3, max_length=32)
    email: str= Field(..., min_length=3, max_length=32)
    firstName: str= Field(..., min_length=3, max_length=32)
    lastName: str= Field(..., min_length=3, max_length=32)
    is_active: bool = True
    is_superuser: bool = False
    def __getattribute__(self, __name: str):
        return super().__getattribute__(__name)