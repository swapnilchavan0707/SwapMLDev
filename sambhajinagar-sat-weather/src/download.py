import os, datetime, requests, time
import pandas as pd
from config import LAT, LON, BBOX

def download_weather_history(days=60):
    print(f"Downloading {days} days weather for {LAT},{LON}...")
    try:
        sd = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
        ed = datetime.date.today().isoformat()
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={LAT}&longitude={LON}&start_date={sd}&end_date={ed}&hourly=temperature_2m,relative_humidity_2m,precipitation,cloud_cover&timezone=Asia/Kolkata"
        r = requests.get(url, timeout=30).json()
        df = pd.DataFrame(r['hourly'])
        df.rename(columns={'time':'timestamp','temperature_2m':'temperature','relative_humidity_2m':'humidity','cloud_cover':'cloud_cover'}, inplace=True)
    except Exception as e:
        print(f"API failed {e}")
        return None

    def label_row(r):
        if r['precipitation'] > 1.0: return "Heavy Rain"
        elif r['precipitation'] > 0.1: return "Light Rain"
        elif r['cloud_cover'] > 70: return "Cloudy"
        else: return "Clear"
    df['condition'] = df.apply(label_row, axis=1)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/labels.csv", index=False)
    print(f"Saved {len(df)} rows to data/processed/labels.csv")
    return df

def download_satellite_bulk(hours=6):  # reduced to 6 for quick test
    print(f"Downloading last {hours} hours of Himawari-8 IR...")
    os.makedirs("data/raw", exist_ok=True)
    bbox_str = f"{BBOX['lon_min']},{BBOX['lat_min']},{BBOX['lon_max']},{BBOX['lat_max']}"
    count=0
    for h in range(hours):
        ts = datetime.datetime.utcnow() - datetime.timedelta(hours=h)
        ts = ts.replace(minute=0, second=0, microsecond=0)
        time_str = ts.strftime("%Y-%m-%dT%H:00:00Z")
        url = f"https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME={time_str}&BBOX={bbox_str}&CRS=EPSG:4326&LAYERS=Himawari_AHI_Band13_Clean_Infrared&FORMAT=image/png&WIDTH=256&HEIGHT=256"
        path = f"data/raw/sat_{ts.strftime('%Y%m%d_%H')}.png"
        if os.path.exists(path):
            continue
        try:
            r = requests.get(url, timeout=10)  # 10 sec timeout
            if r.status_code==200 and len(r.content)>5000:
                open(path,'wb').write(r.content)
                count+=1
                print(f"  -> {path} ({len(r.content)} bytes)")
            else:
                print(f"  Skip {time_str}: status {r.status_code}")
        except Exception as e:
            print(f"  Failed {time_str}: {e}")
        time.sleep(1)
    print(f"Downloaded {count} new satellite images - if 0, it's okay, RF model still works!")

if __name__ == "__main__":
    download_weather_history(60)
    download_satellite_bulk(6)