import os
import pandas as pd
from utils.sqlite_handler import SQLiteHandler

class Extraction:
    def read_file(self, path, name):
        db_file = os.path.join(path, f"{name}.db")
        csv_file = os.path.join(path, f"{name}.csv")

        # Check if the CSV file exists
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found at {csv_file}")

        # Initialize SQLiteHandler
        sqlite_handler = SQLiteHandler(db_file, csv_file, name)
        data_set = sqlite_handler.load_data()

        # Read CSV
        try:
            df = pd.read_csv(csv_file)
            return df
        except Exception as e:
            print(f"Error reading the CSV file: {e}")
            return None

extractor = Extraction()
df = extractor.read_file('data/', 'data_set')

if df is not None:
    print("Dataframe loaded successfully.")
else:
    print("Failed to load dataframe.")
