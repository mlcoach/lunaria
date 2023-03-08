
from dataclasses import dataclass
from pydantic import  Field

@dataclass
class UserRegisterRequestDTO():
    username: str = Field(..., min_length=3, max_length=15, regex="^[a-zA-Z0-9_]*$")
    password: str = Field(..., min_length=3, max_length=32, regex="^[a-zA-Z0-9_]*$")
    email: str= Field(..., min_length=3, max_length=32,regex=r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    firstName: str= Field(..., min_length=3, max_length=32, regex="^[a-zA-Z0-9_]*$")
    lastName: str= Field(..., min_length=3, max_length=32, regex="^[a-zA-Z0-9_]*$")
    
    def __getattribute__(self, __name: str):
        return super().__getattribute__(__name)
    
  
