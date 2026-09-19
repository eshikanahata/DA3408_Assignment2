import hashlib
import logging
import os

import joblib
import redis
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("spam-api")

app = FastAPI(title="Spam Detection API (with Redis cache)")

model = None
cache = None

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", "300"))


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    label: str


def cache_key(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"predict:{digest}"


@app.on_event("startup")
def load_model_and_cache():
    global model, cache
    model = joblib.load("model.joblib")
    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    logger.info(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}")


@app.get("/healthz")
def healthz():
    if model is None:
        return JSONResponse(status_code=503, content={"status": "loading"})
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    key = cache_key(req.text)

    cached_label = cache.get(key)
    if cached_label is not None:
        logger.info(f"CACHE HIT  key={key[:20]}... text={req.text[:40]!r}")
        return {"label": cached_label}

    logger.info(f"CACHE MISS key={key[:20]}... text={req.text[:40]!r}")
    label = model.predict([req.text])[0]
    cache.set(key, label, ex=CACHE_TTL_SECONDS)
    return {"label": label}
