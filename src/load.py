from data.data_loader import DataLoader
from utils.logging_config import configure_logger
from dvc import api as dvc_api
import pickle

logger = configure_logger(__name__)

if __name__ == "__main__":

    # Pull from DVC remote
    dvc_api.pull()

    data_loader = DataLoader()
    data_set = data_loader.load_data('data/', 'data_set')

    #Split the data in x_train, x_test, y_train, y_test
    data_set.split_data()
    #Pickle the data
    with open('data/data_set.pkl', 'wb') as f:
        pickle.dump(data_set, f)
