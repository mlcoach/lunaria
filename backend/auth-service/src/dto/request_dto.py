import datetime
import os
from pydantic import BaseModel


class RequestDTO(BaseModel):
    id: str #user id
    clientId: str #user token
    exp: datetime #expiration date
    
    def __init__(self, id, clientId):
        
        EXPIRESSECONDS = int(os.getenv('EXPIRESSECONDS')) 

        self.id = id
        self.clientId = clientId

        self.exp = datetime.utcnow() + datetime.timedelta(seconds=EXPIRESSECONDS)