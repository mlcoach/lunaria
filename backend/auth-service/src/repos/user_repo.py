from models.user_model import UserModel

class UserRepository():
    def __init__(self, cluster, keyspace):
        self.session = cluster.connect(keyspace)

    def get(self, user_id):
        return self.session.execute("SELECT * FROM clients WHERE id = %s", (user_id,))
    
    def get_all(self):
        return self.session.execute("SELECT * FROM clients")
    
    def create(self, user):
        pass
    
    def update(self, user):
      pass
    
    def delete(self, user_id):
        return self.session.execute("DELETE FROM clients WHERE id = %s", (user_id,))
