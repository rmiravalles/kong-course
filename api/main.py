from fastapi import FastAPI, Request

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