# 2. FastAPI

## Goal

See the upstream application independently from Kong.

The API container listens on port `8000` inside Docker. It is not published directly to the host, so use the container itself for a direct test:

```bash
docker compose exec api curl -i http://localhost:8000/
docker compose exec api curl -i http://localhost:8000/test
```

Open `api/main.py`. The decorators define the endpoints:

```python
@app.get("/test")
def test():
    return {"message": "Hello from /test"}
```

Add a new endpoint, rebuild, and test it through Kong:

```python
@app.get("/hello")
def hello():
    return {"message": "Hello from a new endpoint"}
```

```bash
docker compose up -d --build
curl -i http://localhost:8100/api/hello
```

## Checkpoint

Identify which 404 comes from FastAPI and which 404 comes from Kong. Compare the `server` header and the response body.
