import logging
import os

def configure_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    path = 'src/logs'
    # Check if directory exists.
    # If not, create it.
    if not os.path.exists(path):
        os.makedirs(path)
    
    # Create a file handler and set its level to DEBUG.
    file_handler = logging.FileHandler(f'{path}/debug.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger.
    logger.addHandler(file_handler)

    return logger