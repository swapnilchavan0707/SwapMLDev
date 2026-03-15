import os

# Get the absolute path of the directory where this __init__.py lives
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Define absolute paths for the project files
# This ensures any script can find the data, regardless of where it is run from.
SALES_CSV = os.path.join(DATA_DIR, 'sales_history.csv')
INVENTORY_DB = os.path.join(DATA_DIR, 'inventory.db')

# Versioning for the data assets
__data_version__ = "1.0.0"

def get_data_path():
    """Returns the absolute path to the data directory."""
    return DATA_DIR