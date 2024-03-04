from data.data_loader import DataLoader
from data.data_preprocessor import DataPreprocessor
from utils.logging_config import configure_logger

logger = configure_logger(__name__)

if __name__ == "__main__":

    data_loader = DataLoader()
    data_set = data_loader.load_data('data/', 'data_set')

    data_preprocessor = DataPreprocessor(data_set)
    preprocessed_dataset = data_preprocessor.preprocess_data()

    if preprocessed_dataset is not None:
        logger.info("Dataset preprocessed successfully.")
    else:
        logger.info("Failed to preprocess dataset.")
