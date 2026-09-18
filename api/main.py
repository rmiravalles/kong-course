from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Hello from FastAPI",
        "source": "fastapi"
    }

@app.get("/test")
def test():
    return {"message": "Hello from /test"}

@app.get("/health")
def health():
    return {"status": "healthy"}