from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model
import uuid

class UserLoginModel(Model):
    __keyspace__ = 'users'
    uid = UUID(primary_key=True, default=uuid.uuid4)
    passwordHash = Text(required=True)
    passwordSalt = Text(required=True)
    confirmationToken = Text(required=False)
    confirmationTokenExpiration = DateTime(required=False)
    emailVerified = Boolean(required=False)
    passwordRecoveryToken = Text(required=False) 
    passwordRecoveryTokenExpiration = DateTime(required=False)
    created_at = DateTime()
    updated_at = DateTime()