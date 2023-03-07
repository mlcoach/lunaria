import hashlib
import uuid
from models.user_login_model import UserLoginModel
from models.error_model import ErrorModel
from constants.error_enum import ErrorEnum

def map_schema(model, to_model):
    same_kwargs = list(set(model.__dict__.keys() )& set(to_model.__dict__.keys()))
    arg_dict = {k: v for k, v in model.__dict__.items() if k in same_kwargs}
    #if model is a userrequestdto and to_model is a userloginmodel then we need to convert the password to a hash
    if to_model == UserLoginModel:
        try:
            arg_dict['passwordSalt'] = uuid.uuid4().hex
            arg_dict['passwordHash'] = hashlib.sha256((model.__getattribute__('password') + arg_dict['passwordSalt']).encode('utf-8')).hexdigest()
        except Exception as e:
            raise ErrorModel(ErrorEnum.PASSWORD_NOT_FOUND, ErrorEnum.PASSWORD_NOT_FOUND.value)
    return to_model(**arg_dict)