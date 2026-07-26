"""
Inference for live prediction
"""
import os, pickle, datetime, numpy as np, requests
from PIL import Image
from io import BytesIO
from config import LAT, LON, BBOX, IMAGE_SIZE

def get_current_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,cloud_cover,precipitation&timezone=Asia/Kolkata"
    r = requests.get(url, timeout=10).json()
    return r['current']

def get_live_satellite_array():
    bbox_str = f"{BBOX['lon_min']},{BBOX['lat_min']},{BBOX['lon_max']},{BBOX['lat_max']}"
    time_str = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00Z")
    sat_url = f"https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME={time_str}&BBOX={bbox_str}&CRS=EPSG:4326&LAYERS=Himawari_AHI_Band13_Clean_Infrared&FORMAT=image/png&WIDTH=512&HEIGHT=512"
    r = requests.get(sat_url, timeout=15)
    img = Image.open(BytesIO(r.content)).convert("L").resize((IMAGE_SIZE, IMAGE_SIZE))
    arr = np.array(img)/255.0
    return arr, sat_url

def predict():
    cur = get_current_weather()
    # RF prediction
    clf_path = "models/weather_classifier.pkl"
    if os.path.exists(clf_path):
        clf = pickle.load(open(clf_path,'rb'))
        X = [[cur['temperature_2m'], cur['relative_humidity_2m'], cur['cloud_cover'], datetime.datetime.now().hour, datetime.datetime.now().month]]
        pred = clf.predict(X)[0]
        print(f"RF Prediction: {pred}, Temp: {cur['temperature_2m']}C")
    # CNN prediction if available
    if os.path.exists("models/sat_cnn.h5"):
        import tensorflow as tf
        model = tf.keras.models.load_model("models/sat_cnn.h5")
        le = pickle.load(open("models/label_encoder.pkl","rb"))
        arr,_ = get_live_satellite_array()
        arr_input = arr[np.newaxis,...,np.newaxis]
        p = model.predict(arr_input)
        pred_cnn = le.inverse_transform([np.argmax(p)])[0]
        print(f"CNN Satellite Prediction: {pred_cnn}")

if __name__ == "__main__":
    predict()