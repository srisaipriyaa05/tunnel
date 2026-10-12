# Redis Hit Counter API

FastAPI + Redis with persistent, atomic per-key counters.

## Endpoints
- `POST /hit/{key}` — Redis `INCR`; returns `{"key":"...","count":N}`.
- `GET /count/{key}` — returns current count or `0` for an unseen key.
- `GET /healthz` — pings Redis and returns `{"status":"ok","redis":"up"}` only when Redis is reachable.

Redis is not published to the host. The API reaches it through Compose DNS at `redis:6379`. A named volume and Redis AOF enable persistence across container restarts.

## Run locally
Requires Docker Engine/Desktop with the Compose plugin:
```bash
docker compose up --build -d
docker compose ps
curl -i http://localhost:8000/healthz
curl -i -X POST http://localhost:8000/hit/demo
curl -i http://localhost:8000/count/demo
```

Expected sequence for a fresh `demo` key: count `1`, then `1`.

## Expose a public tunnel
Keep the stack running. In a second terminal, run either:

Cloudflare Tunnel:
```bash
cloudflared tunnel --url http://localhost:8000
```

Or LocalTunnel:
```bash
npx localtunnel --port 8000
```

Use the HTTPS URL printed by the tunnel as the submission base URL. Keep the tunnel process and Docker Compose stack running while the grader tests the endpoint. A temporary tunnel URL changes if the tunnel process is restarted.

## Important
This ZIP contains the stack source/configuration. It cannot start Docker or create a public tunnel on your machine from here; run the commands above on the computer that will host the stack.
