from fastapi import FastAPI
from fastapi.responses import JSONResponse
from deploy.dto.service_register_dto import ServiceRegisterDto
from deploy.service.service_register_service import ServiceRegisterS
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    host="localhost",
    database="POSTGRES_USER",
    user = "POSTGRES_USER",
    password="POSTGRES_PASSWORD"
)

service_register_service = ServiceRegisterS(conn)


@app.post("/register-service")
def register_service(service_register_dto: ServiceRegisterDto):
    try:
        service_register_service.register_service(service_register_dto)
        return JSONResponse(status_code=200, content={"message": "Service registered successfully"})
    except Exception as e:
        if e.args[0] == "Service already exists":
            return JSONResponse(status_code=409, content={"message": "Service already exists"})
@app.get("/get-services")
def get_services(service_name: str):
    try:
        services = service_register_service.get_services(service_name)
        service_dict = {}
        service_count = 0
        for service in services:
            service_dict[service[1]+'_{}'.format(service_count)] = service[0]
            service_dict[service[1]+'_{}'.format(service_count)+"_user_count"] = service[2]
            service_count += 1
        service_dict["service_count"] = service_count
        return JSONResponse(status_code = 200,
                            content = service_dict)
    except Exception as e:
        raise e
    
@app.delete("/delete-service")
def delete_service(service_url: str):
    try:
        service_register_service.delete_service(service_url)
        return JSONResponse(status_code=200, content={"message": "Service deleted successfully"})
    except Exception as e:
        raise e

@app.put("/update-service")
def update_service(service_url: str, user_count : int):
    try:
        service_register_service.update_service(service_url, user_count)
        return JSONResponse(status_code=200, content={"message": "Service updated successfully"})
    except Exception as e:
        raise e