#TODO: Refactor the code using visitor code and reduce the usage of sql query string

class ServiceRegisterRepo():
    def __init__(self, connection):
        self.connection = connection
    
    def get_services(self, service_name):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM services WHERE service_name = %s", (service_name,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            raise e
    def register_service(self, service_name, service_url, user_count):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO services VALUES (%s, %s, %s)", (service_url, service_name, user_count))
                self.connection.commit()
                return True
        except Exception as e:
            raise e

    def delete_service(self, service_url):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM services WHERE service_ip = %s", (service_url,))
            self.connection.commit()
            return True
        except Exception as e:
            raise e

    def update_service(self,service_url : str, user_count : int):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE services SET user_count = %s WHERE service_ip = %s", (user_count, service_url))
            self.connection.commit()
            return True
        except Exception as e:
            raise e
