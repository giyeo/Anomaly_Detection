import pandas as pd
from io import BytesIO
import time
import random

def create_sample_csv(number_of_points=1000, start_value=0, end_value=200, output_file='sample.csv'):

    current_time = int(time.time())
    timestamps = [current_time + i for i in range(number_of_points)]
    values = [random.uniform(start_value, end_value) for _ in range(number_of_points)]

    data = {
        "timestamp": timestamps,
        "value": values
    }
    df = pd.DataFrame(data)

    df.to_csv(output_file, index=False)

    print(f"Sample data saved to {output_file}")

#get from command line arguments
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = 'sample.csv'
    
    create_sample_csv(output_file=output_file)