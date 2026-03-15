import pandas as pd
import numpy as np
from geopy.distance import geodesic
import os


def process_sensor_data(df):
    """
    Cleans sensor data and calculates travel metrics.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    # Calculate distance traveled between pings (in Kilometers)
    df['dist_km'] = 0.0
    for i in range(1, len(df)):
        prev_coords = (df.iloc[i - 1]['latitude'], df.iloc[i - 1]['longitude'])
        curr_coords = (df.iloc[i]['latitude'], df.iloc[i]['longitude'])
        df.at[i, 'dist_km'] = geodesic(prev_coords, curr_coords).km

    # Calculate cumulative distance
    df['total_distance'] = df['dist_km'].cumsum()

    return df


if __name__ == "__main__":
    # Test Logic
    DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/raw_sensor_stream.csv')
    if os.path.exists(DATA_PATH):
        raw_data = pd.read_csv(DATA_PATH)
        processed = process_sensor_data(raw_data)
        print(f"Processed {len(processed)} sensor pings.")
        print(f"Total Shipment Distance: {processed['total_distance'].max():.2f} km")