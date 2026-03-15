"""
Supply Chain Demand Predictor
Modules for data loading, feature engineering, and model training.
"""

import os

# --- PATH CONSTANTS ---
# This allows any module inside src to reference the project folders easily
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# --- EXPOSING KEY FUNCTIONS ---
# We import these here so we can do: from src import load_and_preprocess
from .data_loader import load_sales_data
from .feature_engineering import create_demand_features
from .train_forecaster import train_regression_model

# Package Metadata
__version__ = "1.0.0"
__project__ = "Supply Chain Forecasting"

# Ensure models directory exists whenever the package is initialized
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)