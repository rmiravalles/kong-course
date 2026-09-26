from fastapi import FastAPI, Request
import asyncio
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Hello from FastAPI",
        "source": "fastapi"
    }


@app.get("/test")
async def test(request: Request):
    return dict(request.headers)


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