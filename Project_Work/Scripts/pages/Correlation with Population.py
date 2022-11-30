import pandas as pd
import sys
import logging
import streamlit as st

sys.path.insert(0, '../')

import population_data_preprocessing
import co2_data_preprocessing
import draw_scatter_plot
import draw_correlation_plot



def population_analysis():
    # Input File Path
    input_path = '../Data/'
    # Logging Data
    logging.basicConfig(filename="logfilename.log", level=logging.INFO)
    # Reading population data
    population_data = pd.read_csv(input_path + 'population_data.csv')
    logging.info('Population File read')
    logging.info('Info of population data ' + str(population_data.shape))
    population_data = population_data_preprocessing.data_preprocessing(population_data)
    logging.info('Population Data Cleaned')
    logging.info('Shape of population Data after cleaning ' + str(population_data.shape))
    # Reading CO2 data
    co2_data = pd.read_csv(input_path + 'co2_emission_ur.csv')
    logging.info('CO2 File read')
    logging.info('Info of CO2 data ' + str(co2_data.shape))
    co2_data = co2_data_preprocessing.data_preprocessing(co2_data)
    logging.info('CO2 Data Cleaned')
    logging.info('Shape of CO2 Data after cleaning ' + str(co2_data.shape))
    # Create Correlation Plot
    logging.info('Correlation Plot function called')
    st.subheader("Correlation between Population and CO2 emission")
    'The plot tells us correlation between Population and CO2 levels for every country.'
    'For 80.32% countries we have a positive correlation between CO2 and Population with the ' \
    'highest for Qatar with 0.9958'
    draw_correlation_plot.correlation_plot(population_data, co2_data)
    'The plot is based on temperature and population data studied between 1997 and 2019'
    logging.info('Correlation Plot function ended')
    # Create scatter plot Total
    logging.info('Scatter Plot for total population function called')
    st.subheader("Distribution of countries based on CO2 emission and Population")
    draw_scatter_plot.scatter_plot(population_data, co2_data)

population_analysis()