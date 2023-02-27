from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model
import uuid
class UserModel(Model):
    __keyspace__ = 'users'
    uid = UUID(primary_key=True, default=uuid.uuid4)
    username = Text(required=True, primary_key=True)
    email = Text(required=True, primary_key=True)
    firstName = Text(required=True)
    lastName = Text(required=True)
    role = UUID(required=True, default=uuid.uuid4)
    is_active = Boolean(default=True)
    is_superuser = Boolean(default=False)
    created_at = DateTime()
    updated_at = DateTime()
    name = "UserModel"
# for account service