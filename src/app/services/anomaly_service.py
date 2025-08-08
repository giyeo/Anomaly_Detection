from app.models.anomaly_model import AnomalyDetectionModel
from app.services.versioning_service import ModelVersioning
from app.schemas.api_schemas import TrainResponse, PredictResponse
from app.models.objects import TimeSeries, DataPoint
from app.database.db_operations import save_model_metadata
from fastapi import HTTPException

model_registry = ModelVersioning()

def train_model(series_id, data):
    ts = TimeSeries(
        data = [
            DataPoint(
                timestamp=data.timestamps[i],value=data.values[i])
                for i in range(len(data.values))
            ]
        )
    model = AnomalyDetectionModel().fit(ts)
    version = model_registry.set_model(series_id, model)

    return TrainResponse(series_id=series_id, version=str(version), points_used=len(data.values))

def predict_model(series_id, data, version):
    try:
        model, v = model_registry.get_model(series_id, version)
    except KeyError as e:
        version = 'latest' if not version else version
        raise HTTPException(status_code=404, detail=f"Model with series_id '{series_id}' and version '{version}' not found")

    anomaly = model.predict(DataPoint(timestamp=data.timestamp,value=data.value))
    return PredictResponse(anomaly=anomaly, model_version=str(v))

def model_info():
    """Returns the number of unique series_ids with trained models."""
    return len(model_registry.models)
