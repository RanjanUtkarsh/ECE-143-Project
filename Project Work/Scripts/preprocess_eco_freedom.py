# import libraries
import pandas as pd
import os


def data_preprocessing(filepath):
    """
    This method is to load dataset and have data preprocessing and cleaning.
    1. Load Datasets
    2. Data Preprocessing
    3. Data Cleaning
    :param filepath: the path of files
    :return: a preprocessed and cleaned data frame
    """
    eco_dic = {"country": [], "year": [], "eco_freedom": []}
    files = os.listdir(filepath)
    for filename in sorted(files):
        if filename == ".DS_Store":
            continue
        year = filename[5:9]
        df = pd.read_excel('./dataset/eco_freedom/' + filename, usecols=['Country Name', 'Financial Freedom'],
                           na_values='N/A')
        for index, row in df.iterrows():
            eco_dic["country"].append(row['Country Name'])
            eco_dic["year"].append(year)
            eco_dic["eco_freedom"].append(row["Financial Freedom"])
    eco_df = pd.DataFrame(eco_dic)
    eco_df = eco_df.fillna(0.0)
    return eco_df

