"""
PyTorch-style dataset but works with sklearn + TF too
Loads satellite .npy + weather label matched by timestamp
"""
import os, glob, re
import numpy as np
import pandas as pd
from datetime import datetime

class SatWeatherDataset:
    def __init__(self, labels_path="data/processed/labels.csv", img_dir="data/processed/images"):
        self.df = pd.read_csv(labels_path, parse_dates=['timestamp']) if os.path.exists(labels_path) else pd.DataFrame()
        self.img_dir = img_dir
        self.files = glob.glob(os.path.join(img_dir, "*.npy"))
        print(f"Dataset: {len(self.df)} labels, {len(self.files)} images")

    def get_matched_data(self):
        """Match each satellite image timestamp with closest weather label"""
        import pathlib
        data=[]
        for img_path in self.files:
            # sat_20250626_14.npy -> 2025-06-26 14:00
            m = re.search(r'sat_(\d{4})(\d{2})(\d{2})_(\d{1,2})', img_path)
            if not m: continue
            ts = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
            # find closest label within 1 hour
            if self.df.empty: continue
            closest = self.df.iloc[(pd.to_datetime(self.df['timestamp']) - pd.to_datetime(ts).tz_localize('Asia/Kolkata')).abs().argsort()[:1]]
            if closest.empty: continue
            img = np.load(img_path)
            data.append((img, closest.iloc[0]['condition'], closest.iloc[0]['temperature']))
        return data

    def get_images_only(self):
        X=[]
        for f in self.files:
            X.append(np.load(f))
        return np.array(X) if X else np.empty((0,64,64))

if __name__ == "__main__":
    ds = SatWeatherDataset()
    matched = ds.get_matched_data()
    print(f"Matched pairs: {len(matched)}")