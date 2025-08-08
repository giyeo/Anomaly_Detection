import numpy as np
from app.models.objects import DataPoint, TimeSeries

class AnomalyDetectionModel:
    def __init__(self, mean: float = 0.0, std: float = 1.0, points_used: int = 0):
        self.mean = mean
        self.std = std
        self.points_used = points_used

    def fit(self, data: TimeSeries) -> "AnomalyDetectionModel":
        values_stream = [d.value for d in data.data]
        self.mean = np.mean(values_stream)
        self.std = np.std(values_stream)
        self.points_used = len(values_stream)
        return self

    def predict(self, data_point: DataPoint) -> bool:
        return (
            data_point.value > self.mean + 3 * self.std 
            # or data_point.value < self.mean - 3 * self.std
            # depending on the data, seems a good idea to check both sides
        )