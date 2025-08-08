from app.models.anomaly_model import AnomalyDetectionModel
from app.database.db_operations import get_model_metadata, save_model_metadata, get_model_last_version
from collections import defaultdict
from typing import Dict, List, Tuple

class ModelVersioning:
    def __init__(self):
        self.models: Dict[str, Dict[int, List[AnomalyDetectionModel]]] = defaultdict(lambda: defaultdict(list))

    def set_model(self, series_id: str, model: AnomalyDetectionModel) -> int:
        """Stores a model and assigns a new version number."""
        last_version = get_model_last_version(series_id)
        new_version = last_version + 1

        if series_id not in self.models:
            self.models[series_id] = defaultdict(list)
        if new_version not in self.models[series_id]:
            self.models[series_id][new_version] = []
        self.models[series_id][new_version].append(model)

        save_model_metadata(series_id, new_version, model.mean, model.std, model.points_used)
        return new_version

    def set_in_memory_model(self, series_id: str, version: int, model: AnomalyDetectionModel):
        """Stores a model in memory without saving to the database."""
        if series_id not in self.models:
            self.models[series_id] = defaultdict(list)
        if version not in self.models[series_id]:
            self.models[series_id][version] = []
        self.models[series_id][version].append(model)


    def get_model(self, series_id: str, version: int) -> Tuple[AnomalyDetectionModel, int]:
        """Retrieves a specific version of a model for a series_id."""
        
        if version is None:
            version = get_model_last_version(series_id)
            if version == 0:
                raise KeyError(f"series_id '{series_id}' not found")
        if series_id in self.models and version in self.models[series_id]:
            return self.models[series_id][version][-1], version
        
        return self.get_model_from_db(series_id, version)

    
    def get_model_from_db(self, series_id: str, version: int) -> Tuple[AnomalyDetectionModel, int]:
        """Fetches model metadata from the database and loads the model."""
        metadata = get_model_metadata(series_id, version)
        if not metadata:
            raise KeyError(f"series_id '{series_id}' not found")
        model = AnomalyDetectionModel(mean=metadata.mean, std=metadata.std, points_used=metadata.points_used)
        self.set_in_memory_model(series_id, version, model)
        return model, metadata.version
