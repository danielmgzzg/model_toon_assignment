import pandas as pd
from utils.logging_config import configure_logger

logger = configure_logger(__name__)


class DataFrameBuilder:
    """
    This class builds the DataFrame.
    """

    def create_marketing_list(
            self,
            customers,
            prediction_prospect,
            prediction_probability,
            id_col,
            prospect_cols=['possible_prospect'],
            chance_cols=['reject_toon_chance', 'buy_toon_chance'],
            sort_cols=['buy_toon_chance', 'reject_toon_chance'],
            ascending_order=[False, True]):
        """
        This method creates the marketing list.
        Args:
            customers (pandas.DataFrame): The DataFrame containing
            the customers. prediction_prospect (numpy.ndarray): The array
            containing the prospect predictions.prediction_probability
            (numpy.ndarray): The array containing the probability predictions.
            id_col (str): The ID column name.
            prospect_cols (list): The prospect column names.
            chance_cols (list): The chance column names.
            sort_cols (list): The sort column names.
            ascending_order (list): The sort order.
        Returns:
            df (pandas.DataFrame): The DataFrame containing the marketing list.
        """
        logger.info("Creating marketing list.")
        customers = customers.reset_index(drop=True)
        prospects = pd.DataFrame(prediction_prospect,
                                 columns=prospect_cols).reset_index(drop=True)
        chances = pd.DataFrame(prediction_probability,
                               columns=chance_cols).reset_index(drop=True)
        df = pd.concat([customers, prospects, chances], axis=1) \
            .rename(columns={id_col: "customer_id"}) \
            .sort_values(sort_cols, ascending=ascending_order)
        return df
