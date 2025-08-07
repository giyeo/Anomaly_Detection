import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from objects import DataPoint, TimeSeries
from datetime import datetime

def plot(ts: TimeSeries):

    # Convert to pandas DataFrame
    df = pd.DataFrame([{
        "timestamp": datetime.fromtimestamp(dp.timestamp),
        "value": dp.value
    } for dp in ts.data])

    # Plot with seaborn
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x="timestamp", y="value", marker="o")

    plt.title("Time Series Plot")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("timeseries_plot.png")
    print("✅ Plot saved as timeseries_plot.png")
