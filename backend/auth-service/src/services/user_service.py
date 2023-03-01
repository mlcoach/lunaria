import datetime
from dto.register.user_register_request_dto import UserRegisterRequestDTO
from models.user_login_model import UserLoginModel
from repos.user_repo import UserRepository
from models.user_model import UserModel
from models.role_model import UserRoles
from utilities.model_mapper import map_schema


class UserService():

    user_repository:UserRepository = None

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_user_by_username(self, model, username):
        try:
            return self.user_repository.get(model, lambda x: x.username == username)
        except Exception as e:
            raise Exception("User not found")
        
    def get_user_by_email(self, model, email):
        try:
            return self.user_repository.get(model, lambda x: x.email == email)
        except Exception as e:
            raise Exception("User not found")
        
    def get_user_by_id(self, model, user_id):
        try:
            return self.user_repository.get(model, lambda x: x.uid == user_id)
        except Exception as e:
            raise Exception("User not found")

    def get_users(self, model):
        return self.user_repository.get_all(model)

    
    def get_user_role_by_id(self, user_role_id):
        try:
            return self.user_repository.get(UserRoles, lambda x: x.uid == user_role_id)
        except Exception as e:
            raise Exception(e)

    def get_user_role_by_name(self, role_name:str):
        try:
            return self.user_repository.get(UserRoles, lambda x: x.name == role_name)
        except Exception as e:
            raise Exception(e)

    def get_all_user_roles(self):
        return self.user_repository.get_all(UserRoles)
    

    def create_user(self, user):
        try:
            user_model, user_login_model = self.__create_models(user)
            self.user_repository.create(user_model,
                                        UserModel,
                                        lambda x: x.username == user.username)

            self.user_repository.create(user_login_model,
                                         UserLoginModel,
                                         lambda x: x.uid == user_model.uid)
        except Exception as e:
            raise e

    
    def update_user(self, user, model,uid):
        user.updated_at = datetime.datetime.now()
        return self.user_repository.update(user, model, lambda x: x.uid == uid)

    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)
    
    def __create_models(self, user: UserRegisterRequestDTO):
        try:
            user_model = map_schema(user, UserModel)
            user_login_model =  map_schema(user, UserLoginModel)
            user_login_model.uid = user_model.uid
            user_role_uid = self.get_user_role_by_name("user").uid
            admin_role_uid = self.get_user_role_by_name("admin").uid
            user_model.role = admin_role_uid if user.is_superuser == True else user_role_uid
            return user_model, user_login_model
        except Exception as e:
            raise Exception(e)