# 🧠 Anomaly Detection API

A FastAPI-based service for detecting anomalies in univariate time series using a simple statistical model.  
Supports multiple `series_id`s with versioning, live inference, and benchmarking.

---

## 🚀 Features

- Train anomaly detection models on timestamped series data (`/fit`)
- Predict if a point is anomalous (`/predict`)
- Support for model versioning and multiple series
- Built-in `/healthcheck` metrics
- Optional Docker & benchmarking tools
- Visualization endpoint (if enabled): `/plot`

---

## 🧪 Quickstart

### 🔧 Local Setup (Python 3.13+)
```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src uvicorn app.main:app --reload
```

### Run with Docker (Optional)
docker-compose up --build

### Access the API:
Swagger Docs: localhost:8000/docs


## 📊 Benchmarking
- A sample.csv is included to simulate training and testing.
- You can generate a new sample with:

```bash
python _create_sample.py
python _benchmark.py
```

### What the benchmark does:
- Trains the model on the sample
- Runs 5,000 inferences using 100 parallel workers

Example output:
```json
Starting benchmark for predict requests...
Number of requests: 5000
Health Check Response:
{
  'series_trained': 1,
  'inference_latency_ms': {'avg': 5.2, 'p95': 26.1},
  'training_latency_ms': {'avg': 12.3, 'p95': 12.3}
}
Benchmarking completed in 11.87 seconds.
Requests per second: 421.20
```

## 📡 Example cURL Requests

### ✅ Health Check
```bash
curl http://localhost:8000/healthcheck
```
📥 Predict Anomaly (specific version)
```bash
curl -X POST 'http://localhost:8000/predict/sensor_1?version=17' \
  -H 'Content-Type: application/json' \
  -d '{
    "timestamp": "1691000240",
    "value": 18
}'
```
📥 Predict Anomaly (latest version)
```bash
curl -X POST 'http://localhost:8000/predict/sensor_1' \
  -H 'Content-Type: application/json' \
  -d '{
    "timestamp": "1691000240",
    "value": 18
}'
```
🧠 Train a New Model
```bash
curl -X POST http://localhost:8000/fit/sensor_1 \
  -H 'Content-Type: application/json' \
  -d '{
    "timestamps": [1691000000, 1691000060, 1691000120, 1691000180, 1691000240],
    "values": [10, 11, 9, 12, 15]
}'
```
