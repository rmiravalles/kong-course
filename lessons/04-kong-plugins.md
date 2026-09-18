# 4. Kong plugins

## Goal

Use the gateway to apply behavior that should not be repeated in every upstream service.

Kong plugins are attached to services, routes, or consumers. Common examples are authentication, rate limiting, CORS, request transformation, and logging.

As a first experiment, add a rate-limiting plugin under the `api` service in `kong/kong.yml`:

```yaml
    plugins:
      - name: rate-limiting
        config:
          minute: 5
          policy: local
```

Recreate Kong and make several requests:

```bash
docker compose up -d --force-recreate kong
for request in 1 2 3 4 5 6; do
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8100/api/test
done
```

Remove the plugin when the experiment is complete so later lessons start from the basic route.

## Checkpoint

Explain why a gateway-level rate limit can protect multiple upstream endpoints without changing FastAPI code.
