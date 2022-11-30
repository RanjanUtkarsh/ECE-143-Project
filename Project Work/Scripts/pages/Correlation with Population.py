import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import geopandas
import os
import sys
import streamlit as st
import logging

sys.path.insert(0, '../')

import population_data_preprocessing
import co2_data_preprocessing
import draw_scatter_plot
import draw_correlation_plot
import temp_analysis
import buzz_words


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
    draw_correlation_plot.correlation_plot(population_data, co2_data)
    logging.info('Correlation Plot function ended')
    # Create scatter plot Total
    logging.info('Scatter Plot for total population function called')
    draw_scatter_plot.scatter_plot(population_data, co2_data)

population_analysis()