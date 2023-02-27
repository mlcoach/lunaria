
import datetime

from pydantic import BaseModel


class ResponseDTO(BaseModel): 
  token: str
  expiration: datetime

  def __init__(self, token: str, expiration: datetime): 
    self.token = token 
    self.expiration = expiration