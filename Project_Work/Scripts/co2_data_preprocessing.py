# population_data_preprocessing.py

# Importing libraries

import pandas as pd
import numpy as np

def rename_cols(df):
    '''
    This function cleans the year column names after removing "year" and ":" from the text
    :param df: Dataframe
    :return:  Updated dataframe
    '''
    for col in df.columns:
        if '[' in col:
            year = col[:4]
            df.rename(columns = {col:year}, inplace = True)
            df[year] = df[year].apply(pd.to_numeric)
    return df

def clean_data(df):
    '''
    This function drops column that do not have any data
    :param df: DataFrame
    :return: Updated DataFrame
    '''
    df = df.replace('..', np.nan)
    df = rename_cols(df)
    df = df.drop(columns = {'Indicator Name', 'Indicator Code', '2020', '2021'})
    df = df.dropna()
    return df

def data_preprocessing(co2_data):
    '''
    This function performs following data preprocessing / cleaning on the data frame
        1. Clean Column Names with Year
        2. Drop column with nan or '..' values
    :param df: DataFrame
    :return: Updated DataFrame
    '''
    co2_data['Series Name'] = 'CO2 emission level'

    return co2_data