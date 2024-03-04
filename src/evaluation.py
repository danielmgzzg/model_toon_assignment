from utils.logging_config import configure_logger

logger = configure_logger(__name__)


class Evaluation:

    def evaluate_model(self, model):
        # Implementation here
        logger.info("Model evaluated")


if __name__ == "__main__":

    evaluation = Evaluation()
