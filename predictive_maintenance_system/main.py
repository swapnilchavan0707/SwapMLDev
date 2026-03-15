import os
import subprocess
import sys

# --- CONFIGURATION ---
# Get the absolute path of the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')


def run_script(script_name):
    """Helper function to run python scripts located in the src folder."""
    script_path = os.path.join(SRC_DIR, script_name)
    print(f"\n--- Running {script_name} ---")

    try:
        # Executes the script and waits for it to finish
        result = subprocess.run([sys.executable, script_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")
        return False


def main():
    print("Starting Predictive Maintenance System Initialization")
    print("========================================================")

    # 1. Step 1: Initialize Database and Import CSV
    # This creates maintenance.db and loads raw_sensors.csv
    if not run_script('database_manager.py'):
        print("Initialization failed at the Database stage.")
        return

    # 2. Step 2: Train the Machine Learning Model
    # This creates failure_model.pkl based on the data in SQLite
    if not run_script('train_model.py'):
        print("Initialization failed at the Training stage.")
        return

    print("\n========================================================")
    print("SUCCESS: System is fully initialized and trained!")
    print("\nTo view your graphs and interactive dashboard, run:")
    print(f"streamlit run src/dashboard.py")
    print("========================================================")


if __name__ == "__main__":
    main()