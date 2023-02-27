from repos.user_repo import UserRepository
from models.user_model import UserModel


class UserService():
    
    user_repository:UserRepository = None

    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    def get_user(self, username):
        try:
            return self.user_repository.get(username)
        except Exception as e:
            raise e
    
    def get_users(self):
        return self.user_repository.get_all()
    
    def create_user(self, user):
        return self.user_repository.create(user)
    
    def update_user(self, user):
        return self.user_repository.update(user)
    
    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)