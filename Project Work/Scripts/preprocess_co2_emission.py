# Import libraries
import pandas as pd
import numpy as np


def clean_data(df):
    """
    This method is to recognize Null data and drop unrelated column and rows
    :param df: the dataframe to be cleaned
    :return: cleaned dataframe
    """
    df = df.replace('false', np.nan)
    df = df.drop(columns="unit")
    df = df.drop(index=[193, 194])
    df.fillna(0.0)
    return df


def data_preprocessing(df):
    """
    This method is to clean data and transform columns: 1999, 2000 ..., 2019 to columns year and co2
    1. Clean data
    2. Transform columns
    :param df: dataframe needed to be preprocessed
    :return: preprocessed dataframe
    """

    df = clean_data(df)

    dic = {"country": [], "year": [], "co2": []}
    year_set = list(df.columns)[1:]
    for index, row in df.iterrows():
        for year_idx in range(len(year_set)):
            dic["country"].append(row['Country/Region'])
            dic["year"].append(year_set[year_idx])
            dic["co2"].append(row[year_set[year_idx]])

    processed_co2_df = pd.DataFrame(dic)
    processed_co2_df['year'] = processed_co2_df['year'].astype('int64')

    return processed_co2_df


def pr_combine(pr_df, co2_df):
    """
    This method is to combine CO2 dataframe and political regime dataframe
    :param pr_df: a dataframe
    :param co2_df: a dataframe
    :return: combined dataframe
    """
    combined_df = pd.merge(co2_df, pr_df, how="left", left_on=['country', 'year'],
                           right_on=['Entity', 'Year'])
    combined_df['co2'] = combined_df['co2'].astype('float')
    combined_df = combined_df.drop(columns=["Entity", "Year"])
    combined_df = combined_df.dropna(axis=0)
    combined_df['year'] = combined_df['year'].astype('category')
    return combined_df


def eco_combine(eco_df, co2_df):
    """
    This method is to combine CO2 dataframe and economic freedom dataframe
    :param eco_df: economic freedom dataframe
    :param co2_df: CO2 dataframe
    :return: combined dataframe
    """
    eco_df['year'] = eco_df['year'].astype('int64')
    eco_co2_df = pd.merge(co2_df, eco_df, how="left", left_on=['country', 'year'], right_on=['country', 'year'])
    eco_co2_df = eco_co2_df.dropna(axis=0)
    return eco_co2_df
