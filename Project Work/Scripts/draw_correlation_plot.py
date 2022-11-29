# draw_correlation_plot.py

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import geopandas
import folium
from folium.plugins import HeatMap, HeatMapWithTime
from datetime import datetime, timedelta
import streamlit as st

def plot(df):
    fig = px.scatter(df, y='Corr', symbol='Country')
    return fig


def population_df(df, country):
    temp = df[df['Country Name'] == country]
    temp = temp.T
    column_name_filter = temp.columns[0]
    column_dict_filter = {}
    column_dict_filter[column_name_filter] = 'Population_' + country
    column_dict_filter
    temp.rename(columns=column_dict_filter, inplace=True)
    temp = temp[3:-2]
    temp = temp.reset_index()
    return temp

def co2_df(df, country):
    temp = df[df['Country Name'] == country]
    temp = temp.T
    column_name_filter = temp.columns[0]
    column_dict_filter = {}
    column_dict_filter[column_name_filter] = 'CO2_' + country
    column_dict_filter
    temp.rename(columns=column_dict_filter, inplace=True)
    temp = temp[9:-1]
    temp = temp.reset_index()
    return temp



def correlation_plot(population_data, co2_data):
    population_data_total = population_data[population_data['Series Name'] == 'Population, total']
    population_data_total = population_data_total[:217]
    countries = population_data_total['Country Name']
    countries = list(set(list(countries)))
    co2_data = co2_data[co2_data['Country Name'].isin(countries)]

    dicti = {}

    for country in countries:
        p_df = population_df(population_data_total, country)
        try:
            c_df = co2_df(co2_data, country)
        except:
            continue
        df = p_df.copy()
        df = df.merge(c_df, on='index', how='left')
        name1 = 'Population_' + country
        name2 = 'CO2_' + country
        df[name1] = pd.to_numeric(df[name1], errors='coerce')
        df[name2] = pd.to_numeric(df[name2], errors='coerce')
        corr = df[name1].corr(df[name2])
        dicti[country] = corr

        df = pd.DataFrame(list(dicti.items()))
        df.reset_index()

        df = df.rename(columns={0: 'Country', 1: 'Corr'})

    st.plotly_chart(plot(df))




