# Anomaly_Detection
Anomaly Detection with Python

pip freeze vs requirements.txt comparison with git hooks,
try plotly.express maybe


## Dev stuff
uvicorn controller:app --host 0.0.0.0 --port 8000 --reload

http://localhost:8000/docs

http://localhost:8000/openapi.json

## TODO
- Organize the files in the structured manner.
- Rename file, variables, and stuff.
- Implement SQLlite to allow disk persistency. (not only in-memory)
- Create scripts for both dockerfile and compose.
- Improve readme
- Create a Benchmark based on both test-fit and test-predict (use the health check as well)

All the app is running and persisting only in-memory (for now).
Allow to persist in SQLlite. but use in-memory as a cache to allow read prediction performance
You can kinda cache evict the in-memory artifact, in order for it to fetch form db once in a while.

Features
Train anomaly detection models from timestamped values via API
- Done
Maintain separate models per series_id with versioning support
- Done 
Persist trained models for reuse
- Done
Predict if new points are anomalous given a series_id
- Done
Return model version and prediction
- Done
Report system-level performance metrics (latency, load)
- Done

Optional
Performance Testing: Include benchmarking results under load (e.g. 100 parallel inferences)
- can work on it
Preflight Validation: Reject training data that is insufficient, constant, or invalid
- need to think about it
Visualization Tool: Provide a /plot?series_id=sensor_XYZ&version=v3endpoint to show training data
- already kinda have it, work on it.
Model Versioning: Support retraining of the same series_id, versioning each model
- Done