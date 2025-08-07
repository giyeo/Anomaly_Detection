from app.models.anomaly_model import AnomalyDetectionModel
from app.models.versioning import ModelVersioning
from app.schemas.api_schemas import TrainResponse, PredictResponse
from app.models.objects import TimeSeries, DataPoint

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
    model_registry.set_model(series_id, model)
    version = len(model_registry.models[series_id])

    return TrainResponse(series_id=series_id, version=str(version), points_used=len(data.values))

def predict_model(series_id, data, version):
    try:
        model, v = model_registry.get_model(series_id, version)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    anomaly = model.predict(DataPoint(timestamp=data.timestamp,value=data.value))
    return PredictResponse(anomaly=anomaly, model_version=str(v))
