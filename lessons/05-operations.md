# 5. Operations

## Goal

Build habits for diagnosing and operating an API gateway.

Useful commands:

```bash
docker compose ps
docker compose logs --tail=100 kong
docker compose logs --tail=100 api
curl -i http://localhost:8100/api/test
curl -s http://localhost:8101/routes
```

When debugging a request, check in this order:

1. Is the container running?
2. Does Kong have the route loaded?
3. Did Kong match the request path?
4. What path did the upstream receive?
5. Did the upstream return the response or did Kong generate it?

Before production, add TLS, authentication, centralized logs, metrics, health checks, resource limits, pinned image versions, and automated tests. Do not put credentials in `kong.yml`; use environment variables or a secrets manager for sensitive configuration.

## Final challenge

Add a second FastAPI service and expose it at `/catalog`. Give it a separate Kong service and route. Then add authentication to only that route and document how a client obtains access.
