from app.database.db import SessionLocal
from app.schemas.database_schema import ModelMetadata

def save_model_metadata(series_id, version, mean, std, points_used):
    db = SessionLocal()
    try:
        metadata = ModelMetadata(
            series_id=series_id,
            version=version,
            mean=mean,
            std=std,
            points_used=int(points_used)
        )
        db.add(metadata)
        db.commit()
    finally:
        db.close()

def get_model_last_version(series_id):
    db = SessionLocal()
    try:
        metadata = db.query(ModelMetadata).filter(ModelMetadata.series_id == series_id).order_by(ModelMetadata.version.desc()).first()
        return metadata.version if metadata else 0
    finally:
        db.close()


def get_model_metadata(series_id, version):
    db = SessionLocal()
    try:
        query = db.query(ModelMetadata).filter(ModelMetadata.series_id == series_id)
        if version is not None:
            query = query.filter(ModelMetadata.version == version)
        else:
            query = query.order_by(ModelMetadata.version.desc())
        return query.first()
    finally:
        db.close()
    
