from models.user_model import UserModel

class UserRepository():
    def __init__(self, session):
        self.session = session

    def get(self, username):
        return self.session.execute("SELECT * FROM user_model WHERE username = %s", (username,)).one()
    
    def get_all(self):
        return self.session.execute("SELECT * FROM users")
    
    def create(self, user):

        pass
    
    def update(self, user):
      pass
    
    def delete(self, user_id):
        return self.session.execute("DELETE FROM users WHERE id = %s", (user_id,))
