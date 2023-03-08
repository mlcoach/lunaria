from fastapi import FastAPI

app = FastAPI()

@app.get("/heartbeat")
def read_root():
    return {"Hello": "World"}
