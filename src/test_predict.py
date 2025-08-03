import requests
import random
import time

# -----------------------------
# Config
# -----------------------------
API_URL = "http://localhost:8000/predict/sensor_1"  # Change series_id if needed
VERSION = None  # Example: set to 1 or 2 if you want a specific version

# -----------------------------
# Generate a test data point
# -----------------------------
value = random.uniform(-200, 200)  # Some values will be anomalies
timestamp = str(int(time.time()))

payload = {
    "timestamp": timestamp,
    "value": value
}

# Construct the URL with version if specified
url = API_URL if VERSION is None else f"{API_URL}?version={VERSION}"

# -----------------------------
# Send POST request
# -----------------------------
try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    print("✅ Prediction request successful!")
    print(f"Test value: {value}")
    print(f"Anomaly detected: {result['anomaly']}")
    print(f"Model version used: {result['model_version']}")
except requests.exceptions.RequestException as e:
    print("❌ Error sending request:", e)
