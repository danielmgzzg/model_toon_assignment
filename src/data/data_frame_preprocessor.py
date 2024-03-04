import os
import pandas as pd
import numpy as np

from utils.logging_config import configure_logger

logger = configure_logger(__name__)


class DataFramePreprocessor:
    """
    This class preprocesses the DataFrame.
    Args:
        df (pandas.DataFrame): The DataFrame to preprocess.
    """

    def __init__(self, df):
        self.df = df

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
        columns = self.df.dtypes[self.df.dtypes == dtype].index
        return columns

    def impute_missing_with_median(self, cols):
        """
        This method imputes missing values with the median.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
            cols (pandas.Index): The columns to impute.
        Returns:
            None
        """
        logger.info("Imputing missing values with median.")
        for col in cols:
            if col in self.df.columns:
                fill_val = self.df[col].median()
                self.df[col].fillna(fill_val, inplace=True)

    def fill_na_with_value(self, cols, value):
        """
        This method fills missing values with a specific value.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
            cols (pandas.Index): The columns to impute.
            value (str): The value to fill.
        Returns:
            None
        """
        logger.info(f"Filling missing values with {value}.")
        self.df[cols] = self.df[cols].fillna(value)

    def fill_na_with_mode(self, cols):
        """
        This method fills missing values with the mode.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
            cols (pandas.Index): The columns to impute.
        Returns:
            None
        """
        logger.info("Filling missing values with mode.")
        for col in cols:
            if col in self.df.columns:
                mode_series = self.df[col].mode()
                fill_val = mode_series.head(
                )[0] if not mode_series.empty else np.nan
                self.df[col] = self.df[col].fillna(fill_val)

    def encode_categorical_columns(self, cols):
        """
        This method encodes categorical columns.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
            cols (pandas.Index): The columns to encode.
        Returns:
            None
        """
        logger.info("Encoding categorical columns.")
        self.df = pd.get_dummies(self.df, columns=cols, drop_first=True)

    def standardize_column_names(self):
        """
        This method standardizes the column names.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
        Returns:
            None
        """
        logger.info("Standardizing column names.")
        self.df.columns = self.df.columns.str.lower().str.replace(
            ' ', '_').str.replace('[^a-z0-9_]', '').str.replace('-', '_')

    def save_data_to_csv(self, path):
        """
        This method saves the DataFrame to a CSV file.
        Args:
            df (pandas.DataFrame): The DataFrame to preprocess.
            file_name (str): The name of the file to save.
        Returns:
            None
        """
        logger.info(f"Saving DataFrame to {path}")
        self.df.to_csv(path, index=False)
        logger.info("DataFrame saved successfully.")
        return path
