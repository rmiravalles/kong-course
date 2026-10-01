# 4. Kong plugins

## Goal

See how plugins apply authentication, traffic policy, and rejection at the gateway without adding those concerns to FastAPI endpoints.

## Plugin scope

Plugins can be attached at different scopes. In the current `kong/kong.yml`, the plugins are attached directly to routes:

- `key-auth` and `rate-limiting` are on `api-route`.
- `request-termination` is on `admin-route`.
- `health-route` has no authentication plugin, so it remains available for probes and this exercise.

Route scope limits where a plugin applies. The `/admin` termination plugin returns a response from Kong and prevents this route from reaching the FastAPI `/admin` handler.

## API-key authentication

The configured credential for `client-a` is `abc123`; `client-b` uses `def456`. Try a request without a key, then with a valid one:

```bash
curl -i http://localhost:8100/api/test
curl -i -H 'X-API-Key: abc123' http://localhost:8100/api/test
```

The `key_names` setting tells the plugin to look for the credential in the `X-API-Key` header. The sample credentials are committed to the repository for training and must not be reused as real credentials.

## Per-consumer rate limiting

The route allows five requests per minute per consumer, using the `local` policy. Because `limit_by` is `consumer`, requests from the two configured consumers have separate counters:

```bash
for request in 1 2 3 4 5 6; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -H 'X-API-Key: abc123' http://localhost:8100/api/test
done
```

Expect the first requests to succeed and a request over the configured limit to return `429`. A local counter is appropriate for this one-Kong-node exercise; multiple gateway nodes need a shared strategy if the limit must be consistent across nodes.

## Gateway rejection

Try the `/admin` path:

```bash
curl -i http://localhost:8100/admin
```

The request-termination plugin responds with `403` and `Access denied`. The path matches a Kong route, but the request is terminated before the FastAPI handler runs.

## Checkpoint

For each plugin, identify its route scope, the behavior it adds, and one observable response that demonstrates it. Explain how consumer-based rate limiting differs from a single shared counter.

## Evolution note

Commit `dcaf6c2` added key authentication, a consumer, and the `/admin` rejection route. Commit `300bd44` added consumer-based rate limiting and a second consumer.
