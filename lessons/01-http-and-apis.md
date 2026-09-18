# 1. HTTP and APIs

## Goal

Understand what an API client sends and what a server returns before introducing a gateway.

## The request/response model

An HTTP request has a method, URL path, headers, and sometimes a body. The server responds with a status code, headers, and a response body.

Try these requests through Kong:

```bash
curl -i http://localhost:8100/api/
curl -i http://localhost:8100/api/test
curl -i http://localhost:8100/does-not-exist
```

Observe:

- `200 OK` means the request matched an endpoint and completed successfully.
- `404 Not Found` means the requested resource or route does not exist.
- Kong adds headers such as `Via` and `X-Kong-Request-Id` to proxied responses.

## Checkpoint

Before moving on, explain why `/api/test` can return `200` while `/test` returns a Kong route-matching `404`.
