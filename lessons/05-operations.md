# 5. Timeouts, retries, health checks, and operations

## Goal

Relate upstream behavior to Kong's timeout, retry, and health-check settings, then use logs and the Admin API to investigate failures.

## Start with service timeouts

The `api` service sets `connect_timeout: 1000`, `read_timeout: 2000`, and `write_timeout: 1000`. These values are milliseconds. A timeout is a limit on a stage of the upstream exchange, not a promise that a complete client request always finishes within that many milliseconds. The service also sets `retries: 2`.

The `/slow` endpoint sleeps for five seconds and logs when it starts and ends. Call it and inspect both the response and the Kong/API logs:

```bash
curl -i -w '\nelapsed=%{time_total}s\n' \
	-H 'X-API-Key: abc123' http://localhost:8100/api/slow
docker compose logs --tail=50 kong
docker compose logs --tail=50 api-1 api-2
```

Use this as an observation exercise: record the status, elapsed time, which instance logged the request, and whether Kong attempted another target. Timeout and retry outcomes depend on the configured values and the failure type; do not assume every HTTP error is retried.

## Understand retries

`/unstable` is a deliberately stateful demonstration endpoint. Each FastAPI process returns `503` on its first call and succeeds on subsequent calls. With two replicas, each process has its own counter. Use repeated requests to observe the interaction between application state, target selection, and Kong's retry settings:

```bash
for request in 1 2 3 4; do
	curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/unstable

```

The exact sequence depends on which target receives each request and on Kong's retry behavior. A retry can repeat an operation, so production APIs should make retry safety and idempotency explicit. This endpoint is a teaching fixture, not a retry design pattern.

## Active upstream health checks

The `api-upstream` has active checks configured in `kong/kong.yml`. Kong sends HTTP probes to each target at `/health`:

```yaml
active:
	http_path: /health
	timeout: 1
	healthy:
		interval: 5
		successes: 2
	unhealthy:
		interval: 2
		http_failures: 2
		timeouts: 2
```

Here, the active probe timeout and intervals are in seconds. A target needs two successful checks to be marked healthy. Two HTTP probe failures or two timeouts mark it unhealthy, with the unhealthy checks scheduled every two seconds. The API's `/health` endpoint returns HTTP `200` and JSON, so it supplies the probe endpoint expected by this configuration.

These checks go directly from Kong to each upstream target. They are separate from a client's request to Kong's `/health` route, which is forwarded through the service. The configuration currently enables **active** checks only; passive checks are not configured.

Inspect reported target health:

```bash
curl -s http://localhost:8101/upstreams/api-upstream/health
```

Stop one API container and observe requests through the remaining healthy target:

```bash
docker compose stop api-1
curl -s -H 'X-API-Key: abc123' http://localhost:8100/api/test
curl -s http://localhost:8101/upstreams/api-upstream/health
```

Health changes are not necessarily instantaneous: allow the probe interval and failure threshold to elapse. Restart the target and allow two successful checks before expecting it to be considered healthy again:

```bash
docker compose start api-1
```

## Operational debugging loop

Use these commands to check containers, logs, routes, services, and target health:

```bash
docker compose ps
docker compose logs --tail=100 kong
docker compose logs --tail=100 api-1 api-2
curl -s http://localhost:8101/routes
curl -s http://localhost:8101/services
curl -s http://localhost:8101/upstreams/api-upstream/health
```

For a failing request, check in order: are the containers running; is the route loaded; did Kong match it; what path reached FastAPI; is the selected target healthy; and did Kong or FastAPI generate the response? The Admin API is unauthenticated and host-published in this local Compose stack, so keep this setup on a trusted development machine.

## Checkpoint and extension

Explain the difference between a timeout, a retry, an active health check, and a health route. Then extend the upstream with passive checks and predict how they should differ from periodic active probes. Validate the exact passive-check fields against the Kong version you run before changing the declarative config.

## Evolution note

Commit `9a899ba` introduced timeout values and `/slow`; `2f393a3` introduced the unstable endpoint and retries; `c37467b` added the two-target upstream; `8d4f8ed` added active health checks.
