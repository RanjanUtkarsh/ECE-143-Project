import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import geopandas
import streamlit as st


def energy_consumption_per_country(country, df):
    # df for the selected country
    df_country = df[df["Country Name"] == country].drop(
        "Country Name", axis=1).T

    # column name = index, replace it by the country name
    column_name = df_country.columns[0]
    column_dict = {}
    column_dict[column_name] = country
    df_country.rename(columns=column_dict, inplace=True)
    df_country = df_country[3:-7]

    # get the world's mean emission
    world_means = {}
    for yr in range(1990, 2015):
        df1 = df.copy()
        final_yr = str(yr) + ' ' + '[YR'+str(yr)+']'
        df1.drop(df.index[df[final_yr] == '..'], inplace=True)
        world_mean = np.mean(df1[final_yr].astype(float))
        world_means[yr] = world_mean

    # create a line chart for the world's mean
    fig = px.line(world_means.values(), x=df_country.index, y=world_means.values(),
                  color_discrete_sequence=["red"],
                  title=f"Evolution of Energy Consumption for {country}",
                  template="plotly_dark")

    # create a bar chart for the selected country
    fig2 = px.histogram(df_country, x=df_country.index, y=country,
                        color_discrete_sequence=["#4ADEDE"],
                        text_auto=True)

    # add the barchart to the first fig
    fig.add_trace(fig2.data[0])

    # center title
    fig.update_layout(title_x=0.5)
    # rotate tick labels
    fig.update_xaxes(tickangle=45)
    # hide y axe
    fig.update_yaxes(visible=False)

    st.plotly_chart(fig)
