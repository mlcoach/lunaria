from fastapi import FastAPI

app = FastAPI()

@app.get("/heartbeat", status_code=200)
async def heartbeat():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)