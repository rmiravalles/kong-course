# Kong From Zero to Hero

A hands-on learning path for API fundamentals and Kong Gateway, built around a small FastAPI service.

The course starts with plain HTTP and a local API, then adds Kong as the gateway that clients use to reach the service. Every step is runnable with Docker Compose.

## What you will learn

- How to read HTTP requests, responses, status codes, and error sources
- How FastAPI endpoints and request headers work
- How Kong routes, services, upstreams, targets, and `strip_path` fit together
- How Kong plugins provide API-key authentication, per-consumer rate limits, and request termination
- How service timeouts, retries, replicas, and active health checks interact
- How to inspect configuration and debug requests using logs and the Admin API

## Prerequisites

- Git
- Docker Engine with Docker Compose
- `curl`
- A text editor or VS Code

No Python installation is required for the default exercises because FastAPI runs in a container.

## Start here

Clone the repository and start the stack:

```bash
git clone <your-repository-url>
cd kong-course
docker compose up -d --build
```

Verify the API through Kong. The API containers are reachable only inside the Compose network:

```bash
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/test
```

The `/api/test` response is JSON containing the selected replica name and the request headers received by FastAPI. The values can differ between requests.

Stop the stack when you are done:

```bash
docker compose down
```

## Learning path

Work through the lessons in order. Each lesson has a goal, a small experiment, and a checkpoint.

1. [HTTP and APIs](lessons/01-http-and-apis.md) - understand the request/response model with `curl`.
2. [FastAPI](lessons/02-fastapi.md) - inspect and extend the upstream service.
3. [Kong routing](lessons/03-kong-routing.md) - map public paths to upstream paths.
4. [Kong plugins](lessons/04-kong-plugins.md) - add authentication and traffic controls.
5. [Operations](lessons/05-operations.md) - test, observe, secure, and prepare a gateway for real use.

## Project layout

```text
.
├── api/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── kong/
│   └── kong.yml
├── docker-compose.yaml
└── lessons/
```

- `api/main.py` is the upstream FastAPI application.
- `kong/kong.yml` is Kong's database-less declarative configuration.
- `docker-compose.yaml` runs the API and Kong on a shared Docker network.
- `lessons/` contains the guided course.

## Useful endpoints

| URL | Purpose |
| --- | --- |
| `http://localhost:8100/api/` | FastAPI root endpoint; requires `X-API-Key` |
| `http://localhost:8100/api/test` | Replica and request-header details; requires `X-API-Key` |
| `http://localhost:8100/health` | Health endpoint routed through Kong |
| `http://localhost:8100/admin` | Demonstration route terminated with `403` |
| `http://localhost:8101` | Unauthenticated Kong Admin API; local development only |
| `http://localhost:8101/routes` | Inspect loaded routes |
| `http://localhost:8101/services` | Inspect loaded services |

## Course rules

Make one change at a time, predict the result, run the request, and compare it with the prediction. When a request fails, inspect the response headers and Kong logs before changing configuration.

## Next projects

After completing the lessons, try adding a versioned API (`/v1`), a separate upstream service, shared rate-limit storage for multiple Kong nodes, passive health checks, TLS, and a CI job that starts the stack and exercises the public endpoints.
