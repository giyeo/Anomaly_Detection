
from pydantic import BaseModel
from typing import List

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