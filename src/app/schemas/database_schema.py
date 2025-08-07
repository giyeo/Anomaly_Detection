from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database.db import Base
from datetime import datetime

class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(String, index=True)
    version = Column(Integer)
    mean = Column(Float)
    std = Column(Float)
    trained_at = Column(DateTime, default=datetime.utcnow)
    model_path = Column(String)
