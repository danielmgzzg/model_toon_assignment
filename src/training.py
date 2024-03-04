import argparse
import pandas as pd

from utils.logging_config import configure_logger

logger = configure_logger(__name__)


class Training:

    def train_model(self, df):
        if df is None:
            logger.error("Dataframe is None")
            return

        logger.info("Dataframe is loaded and ready for training.")


if __name__ == "__main__":

    training = Training()

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data",
                        type=str,
                        help="Path to the preprocessed data")
    args = parser.parse_args()

    if not args.input_data:
        error_msg = f"CSV file not found at {args.input_data}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    else:
        logger.info(f"Preprocessed CSV file found at {args.input_data}")
        df = pd.read_csv(args.input_data)
        training = Training()
        training.train_model(df)
