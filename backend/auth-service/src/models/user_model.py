from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model
import uuid

class UserLoginModel(Model):
    __keyspace__ = 'users'
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
    
class UserModel(Model):
    uid = UUID(primary_key=True, default=uuid.uuid4)
    username = Text(required=True)
    email = Text(required=True)
    firstName = Text(required=True)
    lastName = Text(required=True)
    role = UUID(required=True, default=uuid.uuid4)
    created_at = DateTime()
    updated_at = DateTime()

class UserRolesModel(Model):
    uid = UUID(primary_key=True, default=uuid.uuid4)
    name = Text(required=True)
    created_at = DateTime()