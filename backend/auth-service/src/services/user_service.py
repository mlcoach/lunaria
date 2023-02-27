import datetime
import hashlib
from models.user_login_model import UserLoginModel
from repos.user_repo import UserRepository
from models.user_model import UserModel


class UserService():
    
    user_repository:UserRepository = None

    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    def get_user_by_username(self, model, username):
        try:
            return self.user_repository.get(model, lambda x: x.username == username)
        except Exception as e:
            raise Exception("User not found")
    
    def get_user_by_id(self, model, user_id):
        try:
            return self.user_repository.get(model, lambda x: x.uid == user_id)
        except Exception as e:
            raise Exception("User not found")

    def get_users(self):
        return self.user_repository.get_all()
    
    def create_user(self, user):
        try:
            user_model = self.create_user_model(user)
            self.user_repository.create(user_model,
                                        UserModel,
                                        lambda x: x.username == user.username)
            login_model = self.create_user_login_model(user, user_model.uid)
            self.user_repository.create(login_model,
                                        UserLoginModel,
                                        lambda x: x.uid == user_model.uid)
        except Exception as e:
            raise e

    
    def create_user_model(self, user):
        return UserModel(
            username = user.username,
            email = user.email,
            firstName = user.firstName,
            lastName = user.lastName,
            is_active = user.is_active,
            is_superuser = user.is_superuser,
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now(),          
        )

    def create_user_login_model(self, user, uid):
        return UserLoginModel(
            uid = uid,
            passwordSalt = user.password,
            passwordHash = hashlib.sha256(user.password.encode()).hexdigest(),
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now(),          
        )

    def update_user(self, user):
        return self.user_repository.update(user)
    
    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)