import plotly.express as px
import streamlit as st

def bar_chart(df, country):
    """
    This method is to draw a bar chart showing the mean CO2 emission and economic freedom of a country over the years
    :param df: a dataframe
    :param country: a country name
    :return: a bar chart
    """
    new_df = df.copy()
    countries = set(new_df['country'])
    assert country in countries

    new_df = new_df[new_df.country == country]
    fig2 = px.bar(new_df, x='year', y=['co2', 'eco_freedom'], title=country, barmode="group")

    return st.plotly_chart(fig2)