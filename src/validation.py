import logging

# Configure the logging
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

class Validation:
    def check_missing_values(self, df, cols):
        # Implementation here
        logging.info("Missing values checked!")   

    def check_data_types(self, df, cols):
        # Implementation here
        pass        

    def check_data_range(self, df, cols):
        # Implementation here
        pass
    
validation = Validation();