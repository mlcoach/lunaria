from dataclasses import dataclass
from pydantic import  Field

@dataclass
class UserLoginRequestDTO():
    username: str = Field(..., max_length=15)
    password: str= Field(..., min_length=3, max_length=32)
    email: str= Field(..., max_length=32)
    
    