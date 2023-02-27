from repos.user_repo import UserRepository
from utilities.model_mapper import ModelMapper


class UserService():
    
    user_repository:UserRepository = None
    model_mapper:ModelMapper = ModelMapper()

    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    def get_user(self, user_id):
        return self.user_repository.get(user_id)
    
    def get_users(self):
        return self.user_repository.get_all()
    
    def create_user(self, user):
        return self.user_repository.create(user)
    
    def update_user(self, user):
        return self.user_repository.update(user)
    
    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)