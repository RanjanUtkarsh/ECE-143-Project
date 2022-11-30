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

st.header("Study on Global climate change (CO2 level) and its correlation with human population and economy")
st.image('../Data/poster.jpeg')

population.population_analysis()
gdp.gdp_analysis()
temp_analysis.temperature_analysis()
buzz_words.get_buzz_words()
political.political_analysis()
