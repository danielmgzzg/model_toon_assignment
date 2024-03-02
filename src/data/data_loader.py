import os
from utils.sqlite_handler import SQLiteHandler
from utils.logging_config import configure_logger

logger = configure_logger(__name__)


class DataLoader:

    def load_data(self, path, name):
        """Load data from a CSV file or a SQLite database."""
        db_file = os.path.join(path, f"{name}.db")
        csv_file = os.path.join(path, f"{name}.csv")

        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found at {csv_file}")

        sqlite_handler = SQLiteHandler(db_file, csv_file, name)

        try:
            data_set = sqlite_handler.load_data()
            logger.debug(f"Data loaded from {csv_file}.")
            return data_set
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
