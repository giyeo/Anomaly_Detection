import numpy as np
from objects import DataPoint, TimeSeries

class AnomalyDetectionModel:

    def fit(self, data: TimeSeries) -> "AnomalyDetectionModel":
        values_stream = [d.value for d in data.data]
        self.mean = np.mean(values_stream)
        self.std = np.std(values_stream)
        self.points_used = len(values_stream)
        return self

    def predict(self, data_point: DataPoint) -> bool:
        return (
            data_point.value > self.mean + 3 * self.std 
            or data_point.value < self.mean - 3 * self.std
        )