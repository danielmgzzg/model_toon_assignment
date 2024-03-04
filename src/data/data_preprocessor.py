import pandas as pd
import argparse

from sklearn.model_selection import train_test_split

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

    def __init__(
        self,
        df,
        target_col,
        column_info_path=None,
        test_size=0.2,
        max_iter=10000,
    ):
        self.column_info_path = column_info_path
        self.target_col = target_col
        self.test_size = test_size
        self.max_iter = max_iter
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
        # args = parser.parse_args()

        # self.df_processor.save_data_to_csv(args.output_data)
        # logger.info(
        #     "Preprocessed data saved to data/preprocessed_data_set.csv")
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

    def separate_target_variable(self):
        """
        This method separates the target variable from the feature matrix.
        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            target_col (str): The target column name.
        Returns:
            X (pandas.DataFrame): The feature matrix.
            y (pandas.Series): The target vector.
        """
        if self.df is None or self.target_col is None:
            logger.error("DataFrame or target column name cannot be None.")
            raise ValueError("DataFrame or target column name cannot be None.")
        if self.target_col not in self.df.columns:
            logger.error(f"{self.target_col} does not exist in the DataFrame.")
            raise ValueError(
                f"{self.target_col} does not exist in the DataFrame.")

        self.X = self.df.drop(self.target_col, axis=1)
        self.y = self.df[self.target_col]
        return self.X, self.y

    def split_data(self):
        """
        This method splits the data into training and testing sets.
        Args:
            X (pandas.DataFrame): The feature matrix.
            y (pandas.Series): The target vector.
            test_size (float): The test size for the train-test split.
        Returns:
            X_train (pandas.DataFrame): The training feature matrix.
            X_test (pandas.DataFrame): The testing feature matrix.
            y_train (pandas.Series): The training target vector.
            y_test (pandas.Series): The testing target vector.
        """
        self.separate_target_variable()

        if self.X is None or self.y is None:
            logger.error("Feature matrix or target vector cannot be None.")
            raise ValueError("Feature matrix or target vector cannot be None.")

        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=self.test_size)
        return X_train, X_test, y_train, y_test
