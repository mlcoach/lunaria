import json
import logging
import os
import requests
log = logging.getLogger(__name__)


class ServiceRegistration:
    def __init__(self,
                 host : str = "localhost",
                 port : str = '5432',
                 scheme : str = "https://"
                 ) -> None:
        self.host : str = host
        self.port : str= port
        self.scheme : str = scheme
    def register_service(self, service_name : str, service_url : str, user_count : int):
        try:
            log.info("Registering service")
            log.info("Service name: " + service_name)
            log.info("Service url: " + service_url)
            log.info("User count: " + str(user_count))
            payload = {
                "service_name": service_name,
                "service_url": service_url,
                "user_count": user_count
            }
            request_uri : str = self.scheme + self.host + ":" + self.port + "/register-service"
            print(request_uri)
            response = requests.post(request_uri, json=payload)
            if response.status_code == 409:
                raise Exception("Service already exists")
            elif response.status_code == 200:
                log.info("Service registered successfully")
                return response
        except Exception as e:
            raise e
    def delete_service(self, service_url : str):
        try:
            log.info("Deleting service")
            log.info("Service url: " + service_url)
            payload = {
                "service_url": service_url
            }
            service_uri : str = self.scheme + self.host + ":" + self.port + "/delete-service"
            response = requests.delete(service_uri, params=payload)
            if response.status_code != 200:
                raise Exception("Error deleting service")
            else:
                log.info("Service deleted successfully")
                return response
        except Exception as e:
            raise e
    def update_service(self, service_url : str, user_count : int):
        try:
            log.info("Updating service")
            log.info("Service url: " + service_url)
            log.info("User count: " + str(user_count))
            payload = {
                "service_url": service_url,
                "user_count": user_count
            }
            service_uri = self.scheme + self.host + ":" + self.port + "/update-service"
            response = requests.put(service_uri,
                                    params = payload)
            if response.status_code != 200:
                raise Exception("Error updating service")
            else:
                log.info("Service updated successfully")
                return response
        except Exception as e:
            raise e
    def get_services(self, service_name : str):
        try:
            log.info("Getting services")
            log.info("Service name: " + service_name)
            payload = {
                "service_name": service_name
            }
            service_uri : str = self.scheme + self.host + ":" + self.port + "/get-services"
            print(service_uri)
            response = requests.get(service_uri, params=payload)
            print(response.content)
            if response.status_code != 200:
                raise Exception("Error getting services")
            else:
                log.info("Services retrieved successfully")
                return response
        except Exception as e:
            raise e

if __name__ == '__main__':
    service_registration = ServiceRegistration(host = 'localhost', port = '8000', scheme = 'http://')
    service_registration.get_services("test_service")
    service_registration.delete_service("http://localhost:8422")
    service_registration.get_services("test_service")
    service_registration.update_service("http://localhost:8032", user_count= 20)
    service_registration.get_services("test_service")
