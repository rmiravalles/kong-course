# 1. HTTP and APIs

## Goal

Read HTTP requests and responses, and distinguish an API endpoint from a gateway route.

## Request and response

An HTTP request contains a method, a path, headers, and sometimes a body. The server returns a status code, headers, and usually a body. This course mostly uses `GET`, so requests retrieve data and carry no request body.

Use `curl -i` to include response headers as well as the response body. This checkout already has later-course authentication enabled on `/api`, so the example includes the configured training key:

```bash
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/test
curl -i http://localhost:8100/does-not-exist
```

The `/api/test` response is JSON with an `instance` name and the headers FastAPI received. Its values can vary because two API containers are running and Kong forwards request headers.

## Status codes and where they come from

- `200 OK`: the request completed successfully.
- `401 Unauthorized`: the `/api` route requires a valid API key; authentication is covered in Lesson 4.
- `404 Not Found`: either Kong found no matching route, or the request reached FastAPI but FastAPI has no matching endpoint.
- `429 Too Many Requests`: the configured per-consumer rate limit was exceeded.
- `403 Forbidden`: Kong's `/admin` route rejects the request before it reaches FastAPI.

Compare these two paths. The first does not match a Kong route; the second matches `/api`, which is removed before FastAPI receives `/not-a-fastapi-endpoint`:

```bash
curl -i http://localhost:8100/not-a-kong-route
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/not-a-fastapi-endpoint
```

The status code alone may not tell you which component generated the response. Compare the body and headers, then use the route configuration and logs to confirm the request path.

## A first experiment

Make one prediction before each request, then inspect the status line and response body:

```bash
curl -i http://localhost:8100/health
curl -i http://localhost:8100/admin
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/test
```

Notice that the same HTTP interface is used in all three cases, even though different Kong routes and plugins control what happens.

## Checkpoint

Explain the difference between a URL path, a FastAPI endpoint, and a Kong route. Identify which component is expected to answer each request above, and support your answer with evidence from the response or configuration.

## Evolution note

The initial project commit (`2e769d6`) introduced the API and basic `/api` and `/health` routes. The later commits add authentication, rate limiting, and gateway rejection behavior; the final checkout therefore responds differently from that original baseline.
