from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel
from typing import List, Optional
import time
from collections import defaultdict
import numpy as np
from app.services.versioning_service import ModelVersioning
from app.models.anomaly_model import AnomalyDetectionModel
from app.models.objects import TimeSeries, DataPoint
from app.schemas.api_schemas import TrainData, TrainResponse, PredictData, PredictResponse, Metrics, HealthCheckResponse
from app.services.anomaly_service import train_model, predict_model, model_info

# -----------------------------
# Initialize App
# -----------------------------
router = APIRouter()

# Metrics
training_latencies = []
inference_latencies = []

@router.post("/fit/{series_id}", response_model=TrainResponse, tags=["Training"])
def fit(series_id: str = Path(...), data: TrainData = None):
    
    validate_training_data(data.timestamps, data.values)

    start_time = time.time()
    response: TrainResponse = train_model(series_id, data)

    latency = (time.time() - start_time) * 1000
    training_latencies.append(latency)
    return response


@router.post("/predict/{series_id}", response_model=PredictResponse, tags=["Prediction"])
def predict(
    series_id: str = Path(...),
    data: PredictData = None,
    version: Optional[int] = Query(None)
):
    if not series_id or not data:
        raise HTTPException(status_code=422, detail="Invalid predict data")

    start_time = time.time()

    response: PredictResponse = predict_model(series_id, data, version)

    latency = (time.time() - start_time) * 1000
    inference_latencies.append(latency)
    print(f"Appended inference latency: {latency}, total: {len(inference_latencies)}")

    return response


@router.get("/healthcheck", response_model=HealthCheckResponse, tags=["Health Check"])
def health_check():
    series_trained = model_info()

    def calc_metrics(latencies):
        if not latencies:
            return Metrics(avg=0, p95=0)
        avg = sum(latencies) / len(latencies)
        p95 = np.percentile(latencies, 95)
        return Metrics(avg=avg, p95=p95)

    return HealthCheckResponse(
        series_trained=series_trained,
        inference_latency_ms=calc_metrics(inference_latencies),
        training_latency_ms=calc_metrics(training_latencies)
    )


def validate_training_data(timestamps, values, min_points=5, constancy_eps=1e-6):
    if not timestamps or not values:
        raise HTTPException(status_code=422, detail="Empty training data.")
    
    if len(timestamps) != len(values):
        raise HTTPException(status_code=422, detail="Timestamps and values length mismatch.")

    if len(values) < min_points:
        raise HTTPException(status_code=422, detail=f"At least {min_points} points required.")

    std = np.std(values)
    if std < constancy_eps:
        raise HTTPException(status_code=422, detail="Data is too constant to train a meaningful model.")
