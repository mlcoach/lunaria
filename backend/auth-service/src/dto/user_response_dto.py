from pydantic import Field
from dataclasses import dataclass


@dataclass
class UserResponseDTO():
    uid: str
    username: str
    email: str
    firstName: str
    lastName: str
    role: str
    is_active: bool
    is_superuser: bool
