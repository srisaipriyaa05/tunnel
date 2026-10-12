import os

import redis
from fastapi import FastAPI, HTTPException
from redis.exceptions import RedisError

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=3, socket_timeout=3)

app = FastAPI(title="Redis Hit Counter")


def redis_or_503():
    try:
        redis_client.ping()
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return redis_client


@app.get("/healthz")
def healthz():
    try:
        redis_client.ping()
    except RedisError:
        raise HTTPException(status_code=503, detail={"status": "error", "redis": "down"})
    return {"status": "ok", "redis": "up"}


@app.post("/hit/{key}")
def hit(key: str):
    client = redis_or_503()
    redis_key = f"hit-counter:{key}"
    try:
        count = client.incr(redis_key)
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"key": key, "count": count}


@app.get("/count/{key}")
def count(key: str):
    client = redis_or_503()
    redis_key = f"hit-counter:{key}"
    try:
        value = client.get(redis_key)
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"key": key, "count": int(value) if value is not None else 0}
