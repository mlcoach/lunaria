from dataclasses import dataclass
from pydantic import Field

@dataclass
class ServiceRegisterDto:
    service_name : str = Field(..., min_length=3, max_length=50, example="service_name")
    service_url : str = Field(..., min_length=3, max_length=50, example="http://localhost:5000/auth")
    user_count: int = Field(..., example=1)