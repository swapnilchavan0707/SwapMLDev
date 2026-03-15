"""
Predictive Maintenance System
This package contains modules for database management,
machine learning training, and visualization.
"""

# Importing key functions so they can be accessed directly from 'src'
from .database_manager import initialize_db
from .train_model import train_predictive_model

# Metadata for the project
__version__ = "1.0.0"
__author__ = "Gemini AI Project"

# Define what is exported when someone uses 'from src import *'
__all__ = ["initialize_db", "train_predictive_model"]