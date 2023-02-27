
from pydantic import BaseModel, Field

class UserRegisterRequestDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=15)
    password: str = Field(..., min_length=3, max_length=32)
    email: str= Field(..., min_length=3, max_length=32)
    firstName: str= Field(..., min_length=3, max_length=32)
    lastName: str= Field(..., min_length=3, max_length=32)
    role: str = Field(..., min_length=3, max_length=32)
    is_active: bool
    is_superuser: bool
    
    
    
