import logging

# Configure the logging
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

class Preparation:
    def impute_missing_with_median(self, df, cols):
        # Implementation here
        logging.info("Missing values imputed with median")

preparation = Preparation();