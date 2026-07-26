import os
import numpy as np
import pandas as pd


def generate_indian_aqi_data():
    print("Generating historical Indian AQI dataset...")
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai']
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq='D')

    data_list = []
    np.random.seed(101)  # Reproducible trends

    for date in dates:
        month = date.month
        for city in cities:
            # Setting up realistic environmental parameters (e.g., winter pollution spikes in Delhi)
            if city == 'Delhi' and month in [10, 11, 12, 1]:  # Severe Winter Smog Season
                pm25_base, pm10_base, no2_base = 280, 380, 65
            elif city in ['Delhi', 'Kolkata', 'Hyderabad'] and month in [5, 6]:  # Dusty Summer
                pm25_base, pm10_base, no2_base = 90, 180, 35
            elif month in [7, 8, 9]:  # Monsoon cleaning effect
                pm25_base, pm10_base, no2_base = 25, 45, 15
            else:  # Normal baseline conditions
                pm25_base = 65 if city in ['Mumbai', 'Chennai'] else 50
                pm10_base = 110 if city in ['Mumbai', 'Chennai'] else 90
                no2_base = 25

            # Adding variance and calculating AQI approximations
            pm25 = max(5, round(pm25_base + np.random.uniform(-15, 30), 1))
            pm10 = max(10, round(pm10_base + np.random.uniform(-20, 40), 1))
            no2 = max(2, round(no2_base + np.random.uniform(-5, 10), 1))
            so2 = max(1, round(8.0 + np.random.uniform(-3, 5), 1))

            # Simple Indian AQI Sub-index mapping simulation logic
            aqi = int(max(pm25 * 1.3, pm10 * 0.9, no2 * 1.1) + np.random.randint(-10, 15))
            aqi = max(15, min(aqi, 500))  # Max capped standard Indian AQI limit

            data_list.append([date.strftime('%Y-%m-%d'), city, pm25, pm10, no2, so2, aqi])

    df = pd.DataFrame(data_list, columns=['Date', 'City', 'PM2.5', 'PM10', 'NO2', 'SO2', 'AQI'])
    os.makedirs('data', exist_ok=True)
    df.to_csv(os.path.join('data', 'raw_aqi.csv'), index=False)
    print(f"Success! Saved raw dataset with {len(df)} rows at data/raw_aqi.csv")


if __name__ == "__main__":
    generate_indian_aqi_data()
