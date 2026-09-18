# 3. Kong routing

## Goal

Understand how Kong connects a public route to an upstream service.

Open `kong/kong.yml`:

```yaml
services:
  - name: api
    url: http://api:8000
    routes:
      - name: api-route
        paths:
          - /api
        strip_path: true
```

The request flow is:

```text
GET /api/test -> Kong matches /api -> Kong strips /api -> API receives GET /test
```

Inspect the live configuration:

```bash
curl -s http://localhost:8101/routes
curl -s http://localhost:8101/services
```

Experiment with `strip_path`:

1. Change it to `false`.
2. Recreate Kong: `docker compose up -d --force-recreate kong`.
3. Call `curl -i http://localhost:8100/api/test`.
4. Explain why FastAPI now returns 404.
5. Restore `true` and recreate Kong.

## Checkpoint

State the difference between a Kong route path and the path that the upstream application receives.
