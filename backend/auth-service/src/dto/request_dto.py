import datetime
import os
from pydantic import BaseModel


class RequestDTO(BaseModel):
    id: str #user id
    token: str #user token
    exp: datetime #expiration date
    
    def __init__(self, id, token):
        
        EXPIRESSECONDS = int(os.getenv('EXPIRESSECONDS')) 

        self.id = id
        self.token = token

        self.exp = datetime.utcnow() + datetime.timedelta(seconds=EXPIRESSECONDS)