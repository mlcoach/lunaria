import datetime

class UserRepository():
    def __init__(self, session):
        self.session = session

    def get(self, model, filterValue):
        try:
            responses = self.get_all(model)
            response = list(filter(filterValue, responses))
            if response:
                return response[0]
            raise Exception("Record not found")
        except Exception as e:
            raise e
        
    def get_all(self, model):
        return model.objects().all()
    
    def create(self, user,model ,filterValue):
        try:
            response = self.get(model, filterValue)
            if response:
                raise Exception("Record already exists")
        except Exception as e:
            if "Record not found" in str(e):
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
                raise Exception("Record not found")
        
    def delete(self, user_id):
        return self.session.execute("DELETE FROM users WHERE id = %s", (user_id,))
