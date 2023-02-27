from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model
import uuid
class UserModel(Model):
    uid = UUID(primary_key=True, default=uuid.uuid4)
    username = Text(required=True)
    email = Text(required=True)
    firstName = Text(required=True)
    lastName = Text(required=True)
    role = UUID(required=True, default=uuid.uuid4)
    is_active = Boolean(default=True)
    is_superuser = Boolean(default=False)
    created_at = DateTime()
    updated_at = DateTime()

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# for account service