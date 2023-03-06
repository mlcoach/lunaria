from deploy.repos.service_register_repo import ServiceRegisterRepo 
from deploy.dto.service_register_dto import ServiceRegisterDto
class ServiceRegisterS:
    def __init__(self, connection):
        self.service_register_repo : ServiceRegisterRepo = ServiceRegisterRepo(connection)
    def get_services(self, service_name):
        try:
            return self.service_register_repo.get_services(service_name)
        except Exception as e:
            raise e
    
    def register_service(self, service_register_dto: ServiceRegisterDto) -> bool:
        try:
            self.service_register_repo.register_service(service_register_dto.service_name,
                                                        service_register_dto.service_url,
                                                        service_register_dto.user_count)
        except Exception as e:
            raise Exception("Service already exists")
    def delete_service(self, service_url):
        try:
            self.service_register_repo.delete_service(service_url)
        except Exception as e:
            raise e
    def update_service(self, service_url : str, user_count : int):
        try:
            self.service_register_repo.update_service(service_url,
                                                      user_count)
        except Exception as e:
            raise e
    