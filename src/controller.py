from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from typing import List, Optional
from versioning import ModelVersioning
from model import AnomalyDetectionModel
from objects import TimeSeries, DataPoint
import time

from collections import defaultdict
import numpy as np

# -----------------------------
# Data Models
# -----------------------------

class TrainData(BaseModel):
    timestamps: List[int]
    values: List[float]

class TrainResponse(BaseModel):
    series_id: str
    version: str
    points_used: int

class PredictData(BaseModel):
    timestamp: str
    value: float

class PredictResponse(BaseModel):
    anomaly: bool
    model_version: str

class Metrics(BaseModel):
    avg: float
    p95: float

class HealthCheckResponse(BaseModel):
    series_trained: int
    inference_latency_ms: Metrics
    training_latency_ms: Metrics

# -----------------------------
# Initialize App
# -----------------------------
app = FastAPI(title="Time Series Anomaly Detection API")
model_registry = ModelVersioning()

# Metrics
training_latencies = []
inference_latencies = []

# -----------------------------
# Routes
# -----------------------------
@app.post("/fit/{series_id}", response_model=TrainResponse, tags=["Training"])
def train_model(series_id: str = Path(...), data: TrainData = None):
    start_time = time.time()
    if not data.values or not data.timestamps or len(data.values) != len(data.timestamps):
        raise HTTPException(status_code=400, detail="Invalid training data")

    ts = TimeSeries(
        data = [
            DataPoint(
                timestamp=data.timestamps[i],value=data.values[i])
                for i in range(len(data.values))
            ]
        )

    model = AnomalyDetectionModel().fit(ts)
    model_registry.set_model(series_id, model)
    version = len(model_registry.models[series_id])

    latency = (time.time() - start_time) * 1000
    training_latencies.append(latency)

    return TrainResponse(series_id=series_id, version=str(version), points_used=model.points_used)


@app.post("/predict/{series_id}", response_model=PredictResponse, tags=["Prediction"])
def predict_anomaly(
    series_id: str = Path(...),
    data: PredictData = None,
    version: Optional[int] = Query(None)
):
    if not series_id or not data:
        raise HTTPException(status_code=400, detail="Invalid predict data")

    start_time = time.time()
    try:
        model, v = model_registry.get_model(series_id, version)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    data.value
    anomaly = model.predict(DataPoint(timestamp=data.timestamp,value=data.value))

    latency = (time.time() - start_time) * 1000
    inference_latencies.append(latency)

    return PredictResponse(anomaly=anomaly, model_version=str(v))


@app.get("/healthcheck", response_model=HealthCheckResponse, tags=["Health Check"])
def health_check():
    series_trained = sum(len(v) for v in model_registry.models.values())

    def calc_metrics(latencies):
        if not latencies:
            return Metrics(avg=0, p95=0)
        avg = sum(latencies) / len(latencies)
        p95 = np.percentile(latencies, 95)
        return Metrics(avg=avg, p95=p95)

    return HealthCheckResponse(
        series_trained=series_trained,
        inference_latency_ms=calc_metrics(inference_latencies),
        training_latency_ms=calc_metrics(training_latencies),
    )
