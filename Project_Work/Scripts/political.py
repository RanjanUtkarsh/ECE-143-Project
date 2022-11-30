import pandas as pd
import streamlit as st
import preprocess_co2_emission
import preprocess_political_regime
import preprocess_eco_freedom
import draw_map
import draw_bar_chart

def political_analysis():
    input_path = '../Data/'
    co2_data = pd.read_csv(input_path + 'co2_emission.csv')
    co2_df = preprocess_co2_emission.data_preprocessing(co2_data)
    pr_df = preprocess_political_regime.load_data(input_path + 'political-regime.csv')
    pr_co2_df = preprocess_co2_emission.pr_combine(pr_df, co2_df)
    eco_df = preprocess_eco_freedom.data_preprocessing(input_path + 'eco_freedom/')
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
        year = st.sidebar.slider("Select the year you want to see", min_value=min_year, max_value=max_year,
                                 value=min_year, step=1)
        is_compared = st.sidebar.checkbox("Compared with CO2 Emission?")

    draw_map.plot(df, year, datatype)

    with st.sidebar:
        if is_compared:
            years = sorted(set(pr_co2_df.year))
            compared_year = st.sidebar.slider("Please select the year for which you want to see the energy consumption",
                                              min_value=years[0], max_value=years[-1], value=years[0], step=1)
    if is_compared:
        draw_map.plot(pr_co2_df, str(compared_year), 'co2')

    country = st.selectbox("Select which country do you want to see", sorted(set(eco_co2_df.country)))
    draw_bar_chart.bar_chart(eco_co2_df, country)