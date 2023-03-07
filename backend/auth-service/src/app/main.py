import datetime
from fastapi import FastAPI
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from fastapi.staticfiles import StaticFiles


from .dependencies import limiter
from .routes.auth import router as auth_router
from .routes.users import router as users_router

from models.role_model import UserRoles

connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)


app.mount("/static", StaticFiles(directory="templates/static"), name="static")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def root():
    return {"message": "Service is running..."}
