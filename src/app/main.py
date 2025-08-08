from fastapi import FastAPI
from app.controllers.anomaly_controller import router as anomaly_router
from app.database.db import Base, engine
from app.schemas.database_schema import ModelMetadata

# Used in order to create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Time Series Anomaly Detection API")

app.include_router(anomaly_router)
