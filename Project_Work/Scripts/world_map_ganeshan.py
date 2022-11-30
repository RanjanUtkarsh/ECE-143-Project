import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import geopandas
import streamlit as st


def world_map(df, year, title):
    if title == 'gdp':
        title = "World GDP in "
    else:
        title = "World Energy Consumption in "
    fig = px.choropleth(df, locations=df['Country Code'], color=year,
                        color_continuous_scale='RdYlGn_r', template="plotly_dark",
                        title=title + year)
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=1)
    # center title and set margin
    fig.update_layout(title_x=0.5, margin={"r": 0, "t": 30, "l": 0, "b": 0})
    return fig
    # return fig.show()


def plot(df, yr, title):
    assert isinstance(yr, str)
    assert int(yr) >= 1990 and int(
        yr) <= 2014, "Please provide a year from 1990 and 2014"
    final_yr = yr + ' ' + '[YR'+yr+']'
    df1 = df.copy()
    df1.drop(df.index[df[final_yr] == '..'], inplace=True)
    df1[final_yr] = df1[final_yr].astype(float)
    fig = world_map(df1, final_yr, title)
    # return fig
    st.plotly_chart(fig)
