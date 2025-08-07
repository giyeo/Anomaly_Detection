from app.models.anomaly_model import AnomalyDetectionModel
from collections import defaultdict
from typing import Dict, List, Tuple

class ModelVersioning:
    def __init__(self):
        self.models: Dict[str, List[AnomalyDetectionModel]] = defaultdict(list)

    def set_model(self, series_id: str, model: AnomalyDetectionModel):
        """Stores a new version of a model for a given series_id."""
        self.models[series_id].append(model)

    def get_model(self, series_id: str, version: int) -> Tuple[AnomalyDetectionModel, int]:
        """Retrieves a specific version of a model for a series_id."""
        if series_id not in self.models:
            raise KeyError(f"series_id '{series_id}' not found")
        
        versions = self.models[series_id]

        #if version not declared, return lastest version.
        if not version:
            return versions[-1], len(versions)

        if 0 < version <= len(versions):
            return versions[version - 1], version
        raise KeyError(f"version '{version}' not found for series_id '{series_id}'")

