import joblib
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Spam Detection API")

model = None
VERSION = "v1"


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    label: str


@app.on_event("startup")
def load_model():
    global model
    model = joblib.load("model.joblib")


@app.get("/healthz")
def healthz():
    if model is None:
        return JSONResponse(status_code=503, content={"status": "loading"})
    return {"status": "ok", "version": VERSION}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    label = model.predict([req.text])[0]
    return {"label": label}
