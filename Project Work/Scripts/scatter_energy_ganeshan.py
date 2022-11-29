import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import geopandas
import streamlit as st


def plot_scatter_energy(df, df_co2):

    df1 = df.copy()
    df1 = df1[df1['1990 [YR1990]'] != '..']
    df1 = df1[df1['2014 [YR2014]'] != '..']

    df1['average_Energy_increase_since_1990'] = (
        df1['2014 [YR2014]'].astype(float) - df1['1990 [YR1990]'].astype(float))/25

    df2 = df_co2.copy()
    df2 = df2[df2['1990 [YR1990]'] != '..']
    df2 = df2[df2['2014 [YR2014]'] != '..']

    df2['average_co2_increase_since_1990'] = (
        df2['2014 [YR2014]'].astype(float) - df2['1990 [YR1990]'].astype(float))/25
    df1 = df1[['Country Name', 'average_Energy_increase_since_1990']]
    df2 = df2[['Country Name', 'average_co2_increase_since_1990']]

    df1 = df1.merge(df2, on='Country Name', how='left')
    df1['CO2 vs Energy'] = df1['average_co2_increase_since_1990'] / \
        df1['average_Energy_increase_since_1990']

    fig = px.scatter(df1, x="average_Energy_increase_since_1990", y="average_co2_increase_since_1990",
                     color='CO2 vs Energy', color_continuous_scale=px.colors.sequential.Viridis, hover_data=['Country Name'], title='Co-Relation of CO2 vs Energy Consumption')

    st.plotly_chart(fig)
