# 2. FastAPI

## Goal

Trace a request into the FastAPI application and understand what the application returns to Kong.

## Routes are application code

Open `api/main.py`. FastAPI decorators bind an HTTP method and path to a Python function. Returning a dictionary produces a JSON response. The current application exposes:

| Method and path | Behavior |
| --- | --- |
| `GET /` | Returns a short service identity message |
| `GET /test` | Returns the instance name and request headers |
| `GET /health` | Returns `{"status":"healthy"}` with status `200` |
| `GET /admin` | Returns a message if the request reaches FastAPI |
| `GET /slow` | Waits five seconds, logs before and after, then returns JSON |
| `GET /unstable` | Returns `503` on the first request handled by that process, then success |

The API listens on port `8000` inside the Docker network. Compose does not publish that port to the host. To make a direct request from inside one API container without installing `curl`, use Python's standard library:

```bash
docker compose exec api-1 python -c "from urllib.request import urlopen; print(urlopen('http://localhost:8000/health').read().decode())"
```

This bypasses Kong. In contrast, a client request to `http://localhost:8100/api/test` enters through Kong and then reaches FastAPI.

## Request data and replicas

`GET /test` accepts a FastAPI `Request` and reports the headers received by the application. The `INSTANCE_NAME` environment variable labels each container, making it possible to tell which replica served a request. Values such as the `Host` header can differ between the client-facing request and the upstream-facing request; inspect rather than assume.

Try the routed request:

```bash
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/test
```

The key is required by the current Kong config. It is a demonstration credential, not a secret-management pattern.

## Add an endpoint

Add this function to `api/main.py`:

```python
@app.get("/hello")
def hello():
    return {"message": "Hello from a new endpoint"}
```

Rebuild both API replicas, then call the endpoint through the existing `/api` route:

```bash
docker compose up -d --build api-1 api-2
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/hello
```

Kong removes the `/api` prefix, so FastAPI receives `GET /hello`. Adding an application endpoint does not require a new Kong route as long as it is under the existing `/api` prefix.

## Checkpoint

Compare a direct request to `api-1:8000/health` with a request through Kong. Which components does each request pass through? Explain why `/api/hello` maps to the FastAPI path `/hello`.

## Evolution note

The initial commit created the root, test, and health endpoints. Commits `dcaf6c2`, `9a899ba`, `2f393a3`, and `c37467b` successively added request inspection, the slow endpoint, controlled `503` behavior, and replica identification.
