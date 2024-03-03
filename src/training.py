import os
# import pandas as pd

from utils.logging_config import configure_logger

logger = configure_logger(__name__)


class Training:

    def train_model(self, df):
        if df is None:
            logger.error("Dataframe is None")
            return

        logger.info("Dataframe is loaded and ready for training.")


training = Training()

csv_file = os.path.join('data/', 'processed_data_set.csv')

# if not os.path.exists(csv_file):
#     raise FileNotFoundError(logger.error("CSV file not found at {csv_file}"))
# else:
#     logger.info(f"Preprocessed CSV file found at {csv_file}")

#     df = pd.read_csv(csv_file)
#     training.train_model(df)
