# import libraries
import pandas as pd


def load_data(filepath):
    """
    This method is to load data and categorizing the political strategy of countries.
    1. Load Data
    2. Clean Data
    3. Categorize data
    :param filepath: the path of dataset file
    :return: dataframe
    """
    pr_df = pd.read_csv(filepath)
    pr_df = pr_df.dropna(axis=0)
    pr_df = pr_df.sort_values(by='regime_row_owid', axis=0, ascending=True)
    pr_df.regime_row_owid = pd.cut(pr_df.regime_row_owid, 4, labels=["closed autocracies", "electoral autocracies", "electoral democracies", "liberal democracies"])
    return pr_df





