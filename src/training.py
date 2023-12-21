import logging

# Configure the logging
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
class Training:
    def train_model(self, df):
        # Implementation here
        logging.info("Model trained")

training = Training();
