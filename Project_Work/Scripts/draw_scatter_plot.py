# draw_scatter_plot.py


import plotly.express as px
import streamlit as st


def plot(final_df, year):
    fig = px.scatter(final_df, x='population_' + year, y='co2_' + year, symbol='Country Name')
    return fig
    #fig.show()



def scatter_plot(population_data, co2_data):
    population_data_total = population_data[population_data['Series Name'] == 'Population, total']
    population_data_total = population_data_total[:217]
    countries = population_data_total['Country Name']
    countries = list(set(list(countries)))
    co2_data = co2_data[co2_data['Country Name'].isin(countries)]

    years = ['1997', '1998', '1999',
             '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
             '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
             '2018', '2019', '2020', '2021']

    columns_to_keep = ['Country Name', '1997', '1998', '1999',
                                                   '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
                                                   '2008',
                                                   '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
                                                   '2017',
                                                   '2018', '2019']

    population_data_total = population_data_total[columns_to_keep]

    co2_data = co2_data[columns_to_keep]

    columns = ['1997', '1998', '1999',
               '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
               '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
               '2018', '2019']

    for column in columns:
        population_data_total = population_data_total.rename(columns={column: 'population_' + column})
        co2_data = co2_data.rename(columns={column: 'co2_' + column})

    final_df = population_data_total.merge(co2_data, on='Country Name', how='left')

    year = st.selectbox(
        'Please select the year for which you want to see the Population vs CO2 scatter for countries', columns)
    st.plotly_chart(plot(final_df, year))
