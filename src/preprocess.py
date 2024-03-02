from data.data_loader import DataLoader
from data.data_preprocessor import DataPreprocessor

data_loader = DataLoader()
data_set = data_loader.load_data('data/', 'data_set')

data_preprocessor = DataPreprocessor(data_set)
preprocessed_dataset = data_preprocessor.preprocess_data()

if preprocessed_dataset is not None:
    print("Dataset preprocessed successfully.")
else:
    print("Failed to preprocess dataset.")
