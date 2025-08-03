import requests
import random
import time

# -----------------------------
# Config
# -----------------------------
API_URL = "http://localhost:8000/fit/sensor_1"  # Change series_id if needed

# -----------------------------
# Generate synthetic data
# -----------------------------
timestamps = []
values = []

for i in range(150):
    num = random.uniform(-20, 20)
    # Inject anomalies every 30 points
    if i % 30 == 0:
        num = random.uniform(-150, 150)
    timestamps.append(int(time.time()) + i)
    values.append(num)

payload = {
    "timestamps": timestamps,
    "values": values
}

# -----------------------------
# Send POST request
# -----------------------------
try:
    
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    print("✅ Training request successful!")
    print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print("❌ Error sending request:", e)
