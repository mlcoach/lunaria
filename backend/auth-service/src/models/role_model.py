from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model
import uuid


class UserRoles(Model):
    __keyspace__ = 'users'
    uid = UUID(primary_key=True, default=uuid.uuid4)
    name = Text(required=True, primary_key=True)
    description = Text(required=True)
    created_at = DateTime()
    updated_at = DateTime()
