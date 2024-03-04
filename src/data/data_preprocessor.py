import pandas as pd
import argparse

from .data_frame_preprocessor import DataFramePreprocessor
from utils.logging_config import configure_logger

logger = configure_logger(__name__)


class DataPreprocessor:
    """
    This class preprocesses the data.
    Args:
        df (pandas.DataFrame): The DataFrame to preprocess.
        column_info_path (str): The path to the column info file.
    """

    def __init__(self, df, column_info_path=None):
        self.column_info_path = column_info_path
        self.df_processor = DataFramePreprocessor(df)

    def preprocess_data(self):
        """
        This method preprocesses the data.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
            column_info_path (str): The path to the column info file.
        Returns:
            df (pandas.DataFrame): The preprocessed DataFrame.
        """
        logger.info("Preprocessing data.")
        self.df_processor.standardize_column_names()

        if self.column_info_path is not None:
            logger.debug(f"Reading column info from {self.column_info_path}.")
            column_info = pd.read_csv(self.column_info_path)
            logger.debug(f"Column info: {column_info}.")

        for dtype in ['float64', 'object', 'bool']:
            cols = self.df_processor.get_columns_of_type(dtype)
            if dtype == 'float64':
                self.df_processor.impute_missing_with_median(cols)
            elif dtype == 'object':
                self.df_processor.fill_na_with_value(cols, "unknown")
                self.df_processor.encode_categorical_columns(cols)
            elif dtype == 'bool':
                self.df_processor.fill_na_with_mode(cols)

        logger.debug("Data preprocessing completed.")

        parser = argparse.ArgumentParser()
        parser.add_argument('--output_data',
                            type=str,
                            help='Path for the output dataset')
        args = parser.parse_args()

        self.df_processor.save_data_to_csv(args.output_data)
        logger.info(
            "Preprocessed data saved to data/preprocessed_data_set.csv")
        return self.df_processor.df

    def get_columns_of_type(self, dtype):
        """
        This method gets the columns of a specific data type.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
            dtype (str): The data type.
        Returns:
            columns (pandas.Index): The columns of the specified data type.
        """
        logger.info(f"Getting columns of type {dtype}.")
        return self.df_processor.get_columns_of_type(dtype)

    def get_df(self):
        """
        This method gets the DataFrame.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
        Returns:
            df (pandas.DataFrame): The DataFrame.
        """
        return self.df_processor.df

    def display_missing_values(self):
        """
        This method displays the missing values.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
        Returns:
            missing_values (pandas.Series): The missing values.
        """
        missing_values = self.get_df().isnull().sum()
        logger.info(f"Missing values: {missing_values}")
        return missing_values

    def display_column_names(self):
        """
        This method displays the column names.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
        Returns:
            columns (pandas.Index): The column names.
        """
        columns = self.get_df().columns
        logger.info(f"Column names: {columns}")
        return columns
