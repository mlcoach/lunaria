
from pydantic import BaseModel, Field

class UserRegisterRequestDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=15, regex="^[a-zA-Z0-9_]*$")
    password: str = Field(..., min_length=3, max_length=32, regex="^[a-zA-Z0-9_]*$")
    email: str= Field(..., min_length=3, max_length=32,regex=r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    firstName: str= Field(..., min_length=3, max_length=32, regex="^[a-zA-Z0-9_]*$")
    lastName: str= Field(..., min_length=3, max_length=32, regex="^[a-zA-Z0-9_]*$")
    role: str = Field(..., min_length=3, max_length=32)
    is_active: bool
    is_superuser: bool
    
    
    
