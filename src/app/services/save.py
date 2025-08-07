from app.db import SessionLocal
from app.schemas.database_schema import ModelMetadata

def save_model_metadata(series_id, version, mean, std, path):
    db = SessionLocal()
    try:
        metadata = ModelMetadata(
            series_id=series_id,
            version=version,
            mean=mean,
            std=std,
            model_path=path
        )
        db.add(metadata)
        db.commit()
    finally:
        db.close()
