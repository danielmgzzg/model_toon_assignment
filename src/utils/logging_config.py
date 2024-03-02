import logging
import os
import sys  # Import sys to access stdout


def configure_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Ensuring the directory for logs exists
    path = 'src/logs'
    if not os.path.exists(path):
        os.makedirs(path)

    # File handler for outputting logs to a file
    file_handler = logging.FileHandler(f'{path}/debug.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Stream handler for outputting logs to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
