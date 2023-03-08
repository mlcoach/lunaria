from fastapi.testclient import TestClient
from src.main import *


client = TestClient(app)


# def test_read_main():
#   response = client.get("/")
#   assert response.status_code == 200
#   assert response.json() == {"message": "Service is running..."}

# def test_login():
#   response = client.post("/auth/login", json={"username": "test", "password": "te33st", "email": "test@gmail.com"})
#   if response.status_code == 200: 
#     assert response.json() == {}
#   else:
#     assert response.status_code == 401 

#   print(response.status_code)

# def test_register():
#   response = client.post("/auth/register", json={"username": "test", "password": "test", "email": "test@gmail.com", "firstName": "test", "lastName": "test", "role": "test"})
#   assert response.status_code != 201
  
# def test_register_conflict():
#   response = client.post("/auth/register", json={"username": "test", "password": "test", "email": "test@gmail.com", "firstName": "test", "lastName": "test", "role": "test"})
#   assert response.status_code == 409
  
# def test_validation():
#   response = client.get("/auth/verify", headers={
#     "Authorization": "key"
#   })
#   assert response.status_code == 401
