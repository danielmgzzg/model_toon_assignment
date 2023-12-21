import logging

# Configure the logging
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

class Evaluation:
    def evaluate_model(self, model):
        # Implementation here
        logging.info("Model evaluated")

evaluation = Evaluation();