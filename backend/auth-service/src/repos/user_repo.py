import datetime
from models.error_model import ErrorModel
from constants.error_enum import ErrorEnum

class UserRepository():
    def __init__(self, session):
        self.session = session

    def get(self, model, filterValue):
        try:
            responses = self.get_all(model)
            response = list(filter(filterValue, responses))
            if response:
                return response[0]
            raise ErrorModel(ErrorEnum.RECORD_NOT_FOUND, ErrorEnum.RECORD_NOT_FOUND.value)
        except Exception as e:
            raise e
        
    def get_all(self, model):
        return model.objects().all()
    
    def create(self, user,model ,filterValue):
        try:
            response = self.get(model, filterValue)
            if response:
                raise ErrorModel(ErrorEnum.USER_ALREADY_EXISTS, ErrorEnum.USER_ALREADY_EXISTS.value)
        except ErrorModel as e:
            if e.status_code == ErrorEnum.RECORD_NOT_FOUND.value:
                user.created_at = datetime.datetime.now()
                user.updated_at = datetime.datetime.now()
                user.save()
            else:
                raise e
    
    def update(self, model, user_id, arg_dict):
        try:
            #update the user by given args_dict
            model.objects(uid=user_id).update(**arg_dict)
        except Exception as e:
            if ""'uid'"" in str(e):
                raise ErrorModel(ErrorEnum.RECORD_NOT_FOUND, ErrorEnum.RECORD_NOT_FOUND.value)
        
    def delete(self, user_id):
        return self.session.execute("DELETE FROM users WHERE id = %s", (user_id,))
