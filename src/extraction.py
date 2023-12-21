import logging

# Configure the logging
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

class Extraction:
    def read_csv(self, path):
        # logging message
        logging.info(f"Reading the CSV from {path}")

    def ensure_data_exists(self):
        # Implementation here
        pass


extractor = Extraction(); 

extractor.read_csv('path/to/data.csv');