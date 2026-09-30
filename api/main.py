from fastapi import FastAPI, Request, Response
import asyncio
import logging
import os

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Hello from FastAPI",
        "source": "fastapi"
    }


INSTANCE_NAME = os.getenv("INSTANCE_NAME", "unknown")

@app.get("/test")
async def test(request: Request):
    return {
        "instance": INSTANCE_NAME,
        "headers": dict(request.headers)
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/admin")
def admin():
    return {"message": "Restricted area!"}


@app.get("/slow")
async def slow():
    logger.warning("Starting slow endpoint")
    await asyncio.sleep(5)
    logger.warning("Finished slow endpoint")
    return {"message": "This was slow!"}


attempts = 0

@app.get("/unstable")
async def unstable():
    global attempts
    attempts += 1

    if attempts == 1:
        return Response (
            content='{"message":"Temporary failure"}',
            status_code=503,
            media_type="application/json"
        )
    return {"message": "Success", "attempt": attempts}