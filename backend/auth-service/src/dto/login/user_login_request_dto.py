from pydantic import Field
from dataclasses import dataclass


@dataclass
class UserLoginRequestDTO():
    username: str | None = Field(default=None, min_length=3, max_length=32,
                                regex="^[a-zA-Z0-9_]*$")

    password: str = Field(..., min_length=3, max_length=32,
                          regex="^[a-zA-Z0-9_]*$")

    email: str | None = Field(default=None, min_length=3, max_length=32,
                              regex=r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
