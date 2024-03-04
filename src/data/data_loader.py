import os
from utils.sqlite_handler import SQLiteHandler
from utils.logging_config import configure_logger
from sklearn.model_selection import train_test_split

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

    def separate_x_y(self, data_set):
        """Separate the data into features and labels."""
        x = data_set.drop(columns=["target"])
        y = data_set["target"]
        logger.info("Data separated into features and labels.")
        return x, y

    def split_data(self):
        """Split the data into training and testing sets."""
        x_train, x_test, y_train, y_test = train_test_split(
            self.x, self.y, test_size=self.test_size, random_state=42)
        logger.info("Data split completed.")
        return x_train, x_test, y_train, y_test
