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
import population
import gdp
import political

st.set_page_config(
    page_title="Project ECE 143",
    page_icon="👋",
)
st.header("Study on Global climate change (CO2 level) and its correlation with human population and economy")
st.image('../Data/poster.jpeg')
st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Welcome to the dashboard that shows how Global climate change(particularly CO2) correlates with different
    geographical and economical factors.
    
    This dashboard is a part of project for course ECE 143 - Programming for Data Analysis 
    
    Through this project we will try to better understand to better understand the major 
    causes/effects of rise in CO2 levels.
"""
)

# population.population_analysis()
# gdp.gdp_analysis()
# temp_analysis.temperature_analysis()
# buzz_words.get_buzz_words()
# political.political_analysis()
