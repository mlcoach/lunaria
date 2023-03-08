from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import requests
import logging
from logging import config


from .dependencies import limiter
from .routes.auth import router as auth_router
from .routes.users import router as users_router


app = FastAPI(title="Auth Service", version="1.0.0")

path = Path(__file__).with_name("log_conf.conf").resolve()

config.fileConfig(path, disable_existing_loggers=False)

app.include_router(auth_router)
app.include_router(users_router)


app.mount("/static", StaticFiles(directory="templates/static"), name="static")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.on_event("startup")
async def startup_event():
    try:
        requests.post("http://localhost:5432/registry", json={
            "service_name": "service_name",
            "service_url": "http://localhost:5000/api/v1",
            "user_count": 0
        })
    except:
        return
        exit()


@app.on_event("shutdown")
async def shutdown_event():
    try:
        requests.delete("http://localhost:5432/registry", json={
            "service_url": "http://localhost:5000/api/v1",
        })
    except:
        return
        exit()


@app.get("/")
async def root(request: Request):
    logging.info("Service is running...")
    return {"message": "Service is running..."}
