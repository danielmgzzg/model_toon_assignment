import os
import pandas as pd
import sqlite3
from .logging_config import configure_logger


logger = configure_logger(__name__)

class SQLiteHandler:
    """
    This class handles SQLite operations.
    Args:
        sqlite_file (str): The SQLite file path.
        csv_file (str): The CSV file path.
        table_name (str): The table name.
    """
    def __init__(self, sqlite_file='src/data/data.db', csv_file=None, table_name=None):
        self.sqlite_file = sqlite_file
        self.csv_file = csv_file
        self.table_name = table_name

    def load_data(self):
        """
        This method loads data from SQLite.
        Args:
            sqlite_file (str): The SQLite file path.
            csv_file (str): The CSV file path.
            table_name (str): The table name.
        Returns:
            df (pandas.DataFrame): The DataFrame containing the data.
        """
        try:
            if not self.sqlite_file:
                logger.error("SQLite file path is not provided.")
                raise Exception("SQLite file path is not provided.")

            if os.path.isfile(self.sqlite_file) or self.csv_file:
                if self.table_name:
                    if not os.path.isfile(self.sqlite_file) and self.csv_file:
                        logger.debug("SQLite file doesn't exist and CSV file is provided.")
                        self.migrate_csv_to_sqlite()
                    logger.info("Fetching data from SQLite.")
                    return self.fetch_data_from_sqlite()
                else:
                    logger.error("Table name is not provided.")
                    raise Exception("Table name is not provided.")
            else:
                logger.error("SQLite file doesn't exist and CSV file is not provided.")
                raise Exception("SQLite file doesn't exist and CSV file is not provided.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise Exception(f"An error occurred: {e}")
        
    def migrate_csv_to_sqlite(self):
        """
        This method migrates CSV data to SQLite.
        Args:
            sqlite_file (str): The SQLite file path.
            csv_file (str): The CSV file path.
            table_name (str): The table name.
        Returns:
            None
        """
        try:
            if not self.csv_file:
                logger.error("CSV file is not provided.")
                raise Exception("CSV file is not provided.")
            
            if not self.table_name:
                logger.error("Table name is not provided.")
                raise Exception("Table name is not provided.")

            # Read CSV file
            df = pd.read_csv(self.csv_file)
            
            # Connect to SQLite database
            with sqlite3.connect(self.sqlite_file) as conn:
                # Convert DataFrame to SQLite table
                logger.info("Converting DataFrame to SQLite table.")
                df.to_sql(self.table_name, conn, if_exists='replace', index=False)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise Exception(f"An error occurred: {e}")

    def fetch_data_from_sqlite(self):
        """
        This method fetches data from SQLite.
        Args:
            sqlite_file (str): The SQLite file path.
            table_name (str): The table name.
        Returns:
            df (pandas.DataFrame): The DataFrame containing the data.
        """
        try:
            if not self.sqlite_file:
                logger.error("SQLite file is not provided.")
                raise Exception("SQLite file is not provided.")

            if not self.table_name:
                logger.error("Table name is not provided.")
                raise Exception("Table name is not provided.")

            # Connect to SQLite database
            with sqlite3.connect(self.sqlite_file) as conn:
                logger.info("Fetching data from SQLite.")
                # Fetch data from SQLite table into a DataFrame
                df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", conn)
            
            logger.info("Data fetched successfully.")
            return df
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise Exception(f"An error occurred: {e}")