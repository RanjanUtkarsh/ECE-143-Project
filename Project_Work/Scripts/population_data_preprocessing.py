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
    df = df.dropna()
    df = rename_cols(df)
    df = df.drop(columns = {'Series Code'})
    return df

def select_age_group(df, age_group_list, age_group_type):
    '''
    This function creates various age groups in population data
    :param df: DataFrame
    :param age_group_list: List of age groups
    :param age_group_type: New age group
    :return: Updated DataFrame
    '''
    new_df = df[df['Series Name'].isin(age_group_list)]
    new_df = new_df.drop(columns = {'Series Name', 'Country Code'})
    new_df_data = new_df.groupby('Country Name').sum()
    new_df_data= new_df_data.reset_index()
    new_df_data['Series Name'] = age_group_type
    return new_df_data

def data_preprocessing(population_data):
    '''
    This function performs following data preprocessing / cleaning on the data frame
        1. Clean Column Names with Year
        2. Drop column with nan or '..' values
        3. Create population age groups based on age
    :param df: DataFrame
    :return: Updated DataFrame
    '''
    population_data = clean_data(population_data)
    country_code = dict(zip(population_data['Country Name'], population_data['Country Code']))
    total_population_data = population_data[population_data['Series Name'] == 'Population, total']
    urban_population = population_data[population_data['Series Name'] == 'Urban population']
    male_population = population_data[population_data['Series Name'] == 'Population, male']
    female_population = population_data[population_data['Series Name'] == 'Population, female']

    young = ['Population ages 00-14, total', 'Population ages 15-19, female', 'Population ages 15-19, male',
             'Population ages 20-24, female',
             'Population ages 20-24, male', 'Population ages 25-29, female', 'Population ages 25-29, male']

    mid = ['Population ages 30-34, female', 'Population ages 30-34, male', 'Population ages 35-39, female',
           'Population ages 35-39, male',
           'Population ages 40-44, female', 'Population ages 40-44, male', 'Population ages 45-49, female',
           'Population ages 45-49, male']

    old = ['Population ages 50-54, female', 'Population ages 50-54, male', 'Population ages 55-59, female',
           'Population ages 55-59, male',
           'Population ages 60-64, female', 'Population ages 60-64, male', 'Population ages 65 and above, female',
           'Population ages 65 and above, male']

    young_population = select_age_group(population_data, young, 'Age below 30')
    mid_population = select_age_group(population_data, mid, 'Age between 30 and 50')
    old_population = select_age_group(population_data, old, 'Age above 50')

    age_group_data = pd.concat([young_population, mid_population, old_population])
    age_group_data['Country Code'] = age_group_data['Country Name'].apply(lambda row: country_code[row])

    population_cleaned = pd.DataFrame()
    population_cleaned = pd.concat(
        [total_population_data, urban_population, male_population, female_population, age_group_data])


    return population_cleaned