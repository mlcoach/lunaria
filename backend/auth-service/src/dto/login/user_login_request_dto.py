from pydantic import BaseModel, Field

class UserLoginRequestDTO(BaseModel):
    username: str = Field(..., max_length=15)
    password: str= Field(..., min_length=3, max_length=32)
    email: str= Field(..., max_length=32)
    
    