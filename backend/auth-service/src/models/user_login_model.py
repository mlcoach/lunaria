from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model
import uuid

class UserLoginModel(Model):
    __keyspace__ = 'clients'
    uid = UUID(primary_key=True, default=uuid.uuid4)
    username = Text(required=True)
    passwordHash = Text(required=True)
    passwordSalt = Text(required=True)
    confirmationToken = Text(required=True)
    confirmationTokenExpiration = DateTime(required=True)
    emailVerified = Boolean(required=True)
    passwordRecoveryToken = Text(required=True) 
    passwordRecoveryTokenExpiration = DateTime(required=True)
    created_at = DateTime()
    updated_at = DateTime()