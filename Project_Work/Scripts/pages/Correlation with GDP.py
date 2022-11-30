import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import geopandas
import streamlit as st
import sys
sys.path.insert(0, '../')

import world_map_ganeshan as world_map_ganeshan
import energy_per_year_ganeshan as energy_per_year_ganeshan
import scatter_gdp_ganeshan as scatter_gdp_ganeshan
import scatter_energy_ganeshan as scatter_energy_ganeshan



def gdp_analysis():
    input_path = '../Data/'

    df = pd.read_csv(
        input_path + '3d932cd6-6f08-4e5d-9f37-28b8e9294cfa_Data_ganeshan.csv')
    df_gdp = pd.read_csv(
        input_path + '460393bc-57e4-4fc9-97af-b26eed59065d_Data_ganeshan.csv')

    df_co2 = pd.read_csv(
        input_path + '86d2850b-7f17-48bb-b051-61ed09aa4227_Data_ganeshan.csv')

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

gdp_analysis()