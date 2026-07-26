"""
Crop & convert satellite PNGs to 64x64 numpy for ML
"""
import os, glob
from PIL import Image
import numpy as np
from config import IMAGE_SIZE

def preprocess_all():
    os.makedirs("data/processed/images", exist_ok=True)
    files = glob.glob("data/raw/*.png")
    print(f"Found {len(files)} raw images")
    for f in files:
        try:
            img = Image.open(f).convert("L") # grayscale IR
            img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
            arr = np.array(img) / 255.0 # normalize 0-1 (colder cloud = brighter = higher)
            # IR: white = cold cloud, so invert? Keep as is for CNN to learn
            out_path = f"data/processed/images/{os.path.basename(f).replace('.png','.npy')}"
            np.save(out_path, arr.astype(np.float32))
        except Exception as e:
            print(f"Failed {f}: {e}")
    print(f"Saved processed to data/processed/images/")

if __name__ == "__main__":
    preprocess_all()