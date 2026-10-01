# 3. Kong routing and upstreams

## Goal

Follow a request from Kong's public listener through a route and service to an upstream target.

## Route, service, upstream, target

In `kong/kong.yml`, these objects have different jobs:

- A **route** matches incoming request properties. `api-route` matches paths beginning with `/api`.
- A **service** describes how Kong reaches an upstream. The `api` service uses host `api-upstream` and port `8000`.
- An **upstream** named `api-upstream` groups backend targets and provides the place to configure health checks.
- A **target** is a concrete backend address. The current targets are `api-1:8000` and `api-2:8000`, resolved through the Docker Compose network.

For `GET /api/test`, the route has `strip_path: true`, so the request flow is:

```text
client /api/test -> Kong matches /api -> Kong removes /api -> upstream receives /test
```

The `/health` route has `strip_path: false`; it forwards `/health` unchanged. The API service's upstream reference is not a URL to one container: it lets Kong select a target from the upstream pool.

## Inspect the running configuration

The Admin API is published on host port `8101` in this local teaching setup:

```bash
curl -s http://localhost:8101/routes
curl -s http://localhost:8101/services
curl -s http://localhost:8101/upstreams
curl -s http://localhost:8101/upstreams/api-upstream/targets
```

The Admin API is exposed without authentication here for local learning only. Do not expose it publicly in a real deployment.

## Observe target selection

Make a few requests and inspect the `instance` value in each response:

```bash
for request in 1 2 3 4; do
  curl -s -H 'X-API-Key: abc123' http://localhost:8100/api/test
  printf '\n'
done
```

Kong balances requests across available targets. A small sample may hit the same target more than once; use the `instance` field to observe rather than infer a strict alternation.

## Route matching versus upstream 404

Compare a path that no Kong route matches with one that matches `/api` but has no corresponding FastAPI endpoint:

```bash
curl -i http://localhost:8100/not-routed
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/not-an-endpoint
```

The first is rejected at Kong's route-matching stage. The second is forwarded to FastAPI as `/not-an-endpoint`, where the application returns `404`.

## Experiment: path rewriting

In `kong/kong.yml`, change `strip_path` to `false` for `api-route`, then reload Kong:

```bash
docker compose up -d --force-recreate kong
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/test
```

FastAPI now receives `/api/test`, which it does not define, and returns `404`. Restore `true` and recreate Kong before continuing.

## Checkpoint

Draw the request path through route, service, upstream, and target. Explain why the service's `host` is `api-upstream` instead of `api-1`, and distinguish a Kong route mismatch from a FastAPI `404`.

## Evolution note

Commit `c37467b` replaced a single `api:8000` service URL with a named upstream and two Compose services. Commit `4449447` corrected the API build paths and dependencies. This is the point in the course where routing becomes load balancing.
