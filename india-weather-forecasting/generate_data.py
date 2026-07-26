import os
import numpy as np
import pandas as pd


def generate_indian_weather_data():
    print("Generating synthetic Indian weather data...")

    # Define cities and seasonal base parameters
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata']
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq='D')

    data_list = []
    np.random.seed(42)  # For reproducible trends

    for date in dates:
        month = date.month
        for city in cities:
            # Base parameters varying by typical Indian monsoon & seasonal metrics
            if month in [5, 6, 7, 8]:  # Summer / Monsoon Season
                base_temp = 34 if city in ['Delhi', 'Kolkata'] else 29
                base_hum = 75 if city in ['Mumbai', 'Kolkata'] else 65
                rain_chance = 0.6 if city in ['Mumbai', 'Kolkata'] else 0.4
            elif month in [11, 12, 1]:  # Winter Season
                base_temp = 14 if city == 'Delhi' else 24
                base_hum = 50
                rain_chance = 0.05
            else:  # Spring / Autumn Transition
                base_temp = 28
                base_hum = 55
                rain_chance = 0.1

            # Introduce realistic random variance
            temp = round(base_temp + np.random.uniform(-4, 5), 1)
            humidity = int(np.clip(base_hum + np.random.randint(-15, 15), 30, 100))
            wind = round(np.random.uniform(5, 25), 1)

            # Monsoon rain generation simulation
            if np.random.rand() < rain_chance:
                rainfall = round(np.random.exponential(scale=15 if city == 'Mumbai' else 8), 1)
            else:
                rainfall = 0.0

            data_list.append([date.strftime('%Y-%m-%d'), city, temp, humidity, rainfall, wind])

    # Format to DataFrame
    df = pd.DataFrame(data_list, columns=['Date', 'City', 'Temperature', 'Humidity', 'Rainfall', 'WindSpeed'])

    # Ensure target output path directory exists
    os.makedirs('data', exist_ok=True)
    csv_path = os.path.join('data', 'raw_weather.csv')

    # Save target dataset
    df.to_csv(csv_path, index=False)
    print(f"Success! Created realistic data file at: {csv_path} ({len(df)} rows generated)")


if __name__ == "__main__":
    generate_indian_weather_data()
