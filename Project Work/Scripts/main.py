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

import population_data_preprocessing
import co2_data_preprocessing
import draw_scatter_plot
import draw_correlation_plot
import temp_analysis
import buzz_words


'----------------------------------------This section is for co2 vs population analysis-----------------------'

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
logging.info('Shape of population Data after cleaning '+ str(population_data.shape))
# Reading CO2 data
co2_data = pd.read_csv(input_path + 'co2_emission.csv')
logging.info('CO2 File read')
logging.info('Info of CO2 data ' + str(co2_data.shape))
co2_data = co2_data_preprocessing.data_preprocessing(co2_data)
logging.info('CO2 Data Cleaned')
logging.info('Shape of CO2 Data after cleaning '+ str(co2_data.shape))
st.header("CO2 data vs Population Correlation")
st.image(input_path+'poster.jpeg')
# Create Correlation Plot
logging.info('Correlation Plot function called')
draw_correlation_plot.correlation_plot(population_data, co2_data)
logging.info('Correlation Plot function ended')
# Create scatter plot Total
logging.info('Scatter Plot for total population function called')
draw_scatter_plot.scatter_plot(population_data, co2_data)

'------------------------------------------------CO2 vs population section complete-------------------------'

'----------------------------------------This section is for World Development Factors GDP and Energy (Ganeshan)-----------------------'

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import geopandas
import streamlit as st

import world_map_ganeshan as world_map_ganeshan
import energy_per_year_ganeshan as energy_per_year_ganeshan
import scatter_gdp_ganeshan as scatter_gdp_ganeshan
import scatter_energy_ganeshan as scatter_energy_ganeshan

input_path = '../Data/'

df = pd.read_csv(
    input_path+'3d932cd6-6f08-4e5d-9f37-28b8e9294cfa_Data_ganeshan.csv')
df_gdp = pd.read_csv(
    input_path+'460393bc-57e4-4fc9-97af-b26eed59065d_Data_ganeshan.csv')

df_co2 = pd.read_csv(
    input_path+'86d2850b-7f17-48bb-b051-61ed09aa4227_Data_ganeshan.csv')

df_co2 = df_co2[:217]
df = df[:217]  # energy df
df_gdp = df_gdp[:217]


years = list(range(1999, 2015))
years = set([str(i) for i in years])

countries = df['Country Name']
countries = list(countries[:217])


year = st.selectbox(
    'Please select the year for which you want to see the energy consumption', years)
world_map_ganeshan.plot(df, year, 'energy')

country = st.selectbox(
    'Please select one country', set(countries))
energy_per_year_ganeshan.energy_consumption_per_country(country, df)

scatter_gdp_ganeshan.plot_scatter_gdp(df_co2, df_gdp)
scatter_energy_ganeshan.plot_scatter_energy(df_co2, df)


'------------------------------------------------World Development Factors section complete-------------------------'

temp_analysis.temperature_analysis()

'------------------------------------------------------------------------------------------------------------'
buzz_words.get_buzz_words()

'----------------------------------------This section is for Political Ideologies and Economic Freedom (Xiao)-----------------------'
import pandas as pd
import streamlit as st
import preprocess_co2_emission
import preprocess_political_regime
import preprocess_eco_freedom
import draw_map
import draw_bar_chart

input_path = '../Data/'
co2_data = pd.read_csv(input_path + 'co2_emission.csv')
co2_df = preprocess_co2_emission.data_preprocessing(co2_data)
pr_df = preprocess_political_regime.load_data(input_path + 'political-regime.csv')
pr_co2_df = preprocess_co2_emission.pr_combine(pr_df, co2_df)
eco_df = preprocess_eco_freedom.data_preprocessing(input_path + 'eco_freedom')
eco_co2_df = preprocess_co2_emission.eco_combine(eco_df, pr_co2_df)

df = None
with st.sidebar:
    st.title('ECE 143 Project')
    datatypes = ("eco_freedom", "politic regime")
    datatype = st.sidebar.selectbox(
        "Which aspect would you like to see?", datatypes)
    if datatype == 'eco_freedom':
        df = eco_co2_df
    else:
        df = pr_co2_df
    min_year = sorted(set(df.year))[0]
    max_year = sorted(set(df.year))[-1]
    year = st.sidebar.slider("Select the year you want to see", min_value=min_year, max_value=max_year, value=min_year, step=1)
    is_compared = st.sidebar.checkbox("Compared with CO2 Emission?")

draw_map.plot(df, year, datatype)

with st.sidebar:
    if is_compared:
        years = sorted(set(pr_co2_df.year))
        compared_year = st.sidebar.slider("Please select the year for which you want to see the energy consumption", min_value=years[0], max_value=years[-1], value=years[0], step=1)
if is_compared:
    draw_map.plot(pr_co2_df, str(compared_year), 'co2')


country = st.selectbox("Select which country do you want to see", sorted(set(eco_co2_df.country)))
draw_bar_chart.bar_chart(eco_co2_df, country)

'-----------------------------Political Ideologies and Economic Freedom section complete----------------------------------'


