import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import time


def simulate_single_ping(last_lat, last_lon, last_temp):
    """
    Generates a single new IoT sensor reading based on the previous state.
    """
    # Simulate movement (moving roughly Northwest)
    new_lat = last_lat + 0.005 + np.random.uniform(-0.001, 0.001)
    new_lon = last_lon - 0.008 + np.random.uniform(-0.001, 0.001)

    # Simulate Temperature with a 10% chance of a sudden spike (Malfunction)
    if np.random.random() > 0.90:
        new_temp = last_temp + np.random.uniform(2.0, 5.0)
    else:
        # Normal fluctuation around 2.0 degrees Celsius
        new_temp = 2.0 + np.random.uniform(-0.5, 0.5)

    return new_lat, new_lon, round(new_temp, 2)


def run_live_simulation(duration_minutes=5, interval_seconds=10):
    """
    Simulates a live stream of data and saves it to the raw_sensor_stream.csv.
    """
    data_path = os.path.join(os.path.dirname(__file__), '../data/raw_sensor_stream.csv')

    # Starting Coordinates (NYC)
    curr_lat, curr_lon = 40.7128, -74.0060
    curr_temp = 2.1

    print(f" Starting IoT Simulation for {duration_minutes} minutes...")

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration_minutes)

    shipment_log = []

    while datetime.now() < end_time:
        curr_lat, curr_lon, curr_temp = simulate_single_ping(curr_lat, curr_lon, curr_temp)

        ping = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "shipment_id": "SHIP_LIVE_001",
            "latitude": curr_lat,
            "longitude": curr_lon,
            "temperature": curr_temp,
            "humidity": round(np.random.uniform(70, 85), 2),
            "vibration": round(np.random.uniform(0.01, 0.4), 3)
        }

        shipment_log.append(ping)

        # Update the CSV file live
        df = pd.DataFrame(shipment_log)
        df.to_csv(data_path, index=False)

        print(f" Ping Sent: Lat {curr_lat:.4f}, Temp {curr_temp}°C")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    # Ensure data folder exists
    os.makedirs(os.path.join(os.path.dirname(__file__), '../data'), exist_ok=True)
    run_live_simulation(duration_minutes=2)