import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import time
import random

def read_sample_csv(file_path='sample.csv'):
    df = pd.read_csv(file_path)
    timestamps = df['timestamp'].tolist()
    values = df['value'].tolist()
    return timestamps, values

def post_request_train_model(series_id, timestamps, values):
    import requests
    url = f"http://localhost:8000/fit/{series_id}"
    data = {
        "timestamps": timestamps,
        "values": values
    }
    response = requests.post(url, json=data)
    return response.json()

def post_request_predict_model(series_id, value):
    import requests
    url = f"http://localhost:8000/predict/{series_id}"
    # class PredictData(BaseModel):
    # timestamp: str
    # value: float
    data = {
        "timestamp": "1754661727",
        "value": value
    }
    response = requests.post(url, json=data)
    #get message detail

    # Debug: print status code and response text
    response.raise_for_status()  # Raises an error for HTTP errors
    return response.json()

def health_check():
    import requests
    url = "http://localhost:8000/healthcheck"
    response = requests.get(url)
    return response.json()

def benchmark_model(series_id, file_path='sample.csv'):
    timestamps, values = read_sample_csv(file_path)
    
    train_response = post_request_train_model(series_id, timestamps, values)
    print(f"Train Response: {train_response}")

    print("Starting benchmark for predict requests...")
    import concurrent.futures

    num_requests = 5000
    print(f"Number of requests: {num_requests}")
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for i in range(num_requests):
            value = random.uniform(0, 200)
            futures.append(executor.submit(post_request_predict_model, series_id, value))
        for future in concurrent.futures.as_completed(futures):
            try:
                predict_response = future.result()
            except Exception as e:
                print(f"Error during prediction: {e}")
    end_time = time.time()
    elapsed = end_time - start_time
    req_per_sec = num_requests / elapsed if elapsed > 0 else 0

    health_check_response = health_check()
    print(f"Health Check Response: {health_check_response}")

    print(f"Benchmarking completed in {elapsed:.2f} seconds.")
    print(f"Requests per second: {req_per_sec:.2f}")

benchmark_model("test_series", "sample.csv")