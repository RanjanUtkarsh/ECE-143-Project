from itertools import count
from sqlite3 import DateFromTicks
from turtle import color
from unicodedata import name
#from zoneinfo import available_timezones
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import os
from plotly.subplots import make_subplots
import streamlit as st

def create_year_labels(years):
    '''
        create_year_labels: creates the year labels that match standard #### [YR####]
        input: array of years
    '''
    labels = []
    for i in years:
        labels.append(str(i) + ' [YR' + str(i) + ']')
    return labels

def get_countries(directory):
    '''
        get_countries: gets the files directory of the data, and creates a list of 
                       of all the countries alpha-3 codes embeded in the file name
        input: directory of data
        type: string
        format: 'data_name_###.csv' where ### represents the 3 letter country code.
    '''
    data_files = os.listdir(directory)

    country_codes = []
    country_names = []
    for i in data_files:
        country_codes.append(i[-7:-4])
        # print(i)
        country_names.append(pycountry.countries.get(alpha_3=i[-7:-4]).name)

    return country_codes, country_names

def get_years_temps(file_name):
    '''
        get_years_temps: gets file name and extracts the years and temperatures for
                        overall country average temperature and returns an array of 
                        the years and the temps
        input: file_name
        type: string
    '''
    df = pd.read_csv(file_name)
    years = []
    temps = []
    for i in range(len(df.index))[1:]:
        years.append(int(df.index[i][0]))
        temps.append(df.index[i][1])
    
    return years, temps

def format_temp_data(df):
    '''
        format_data: changes the dataframe so all data meet a standard
        input: df, dataframe for a countries data
    '''
    df = df.reset_index()
    if df.columns[0] == 'index' and df['index'][0] == 0:
        df = df.drop(['index'], axis=1)
        df = df.drop(df.columns[2:], axis = 1)
    else:
        df = df.drop(df.columns[2:], axis = 1)
        df = df.drop(0, axis=0)

    df.columns = ['years', 'temps']

    return df

def merge_data(file, country_codes, country_names, years):
    '''
        merge_data: extracts data from the data file and merges into a dataframe
                    with all the countries and the corresponding temperatures.
        input: file, file name format of the data
        input: country_codes, codes of the country names
        year: the years to create the data for
    '''
    df_final = pd.DataFrame(0.0,columns=years,index=country_codes).astype(float)
    
    j = 0
    for i in country_codes:
        df = pd.read_csv(file + i + '.csv')
        df = format_temp_data(df)
        df_final.loc[i] = list(df['temps'].astype(float))
        j+=1
    
    return df_final

def format_co2_data(file):
    '''
        format_co2_data: Changes the co2 data to match the temp dataframe
        input: file, path to the co2 data
        type: string
    ''' 
    df = pd.read_csv(file)
    df = df.drop(['Series Name', 'Series Code', 'Country Name',
                  '2020 [YR2020]', '2021 [YR2021]'], axis=1)
    
    df.index = list(df['Country Code'])
    df = df.drop(['Country Code'], axis=1)

    df = df.dropna(axis=0)
    
    df[df.columns] = df[df.columns].astype(float, errors='ignore')
   
    return df

def data_years(df,first_year, last_year):
    '''
        data_years: cuts the data to the given years, from first year to last year
        input: df
        type: dataframe

        input: first_year, last_year
        type: string
        format: #### [YR####]
    '''
    years = list(df.columns)
    years = years[years.index(first_year): years.index(last_year)+1]
 
    return df[years]

def match_data(df1, df2):
    '''
        match_data: Cross checks two dataframes and deletes the uncommon rows and columns
    '''

    df1_rows = list(df1.index)
    df2_rows = list(df2.index)

    common_rows = set(df1_rows) & set(df2_rows)

    uncommon_df1_rows = set(common_rows) ^ set(df1_rows)
    uncommon_df2_rows = set(common_rows) ^ set(df2_rows)

    df1_columns = list(df1.columns)
    df2_columns = list(df2.columns)

    common_columns = set(df1_columns) & set(df2_columns)
    
    df1 = df1.drop(uncommon_df1_rows)
    df2 = df2.drop(uncommon_df2_rows)

    df1 =  df1[sorted(common_columns)]
    df2 =  df2[sorted(common_columns)]

    df1 = df1.sort_index()
    df2 = df2.sort_index()

    return df1, df2

def create_co2_temp_fig(temp_df, co2_df, country):
    '''
    '''

    country_temp = temp_df.loc[country]
    country_co2 = co2_df.loc[country]
    df = pd.DataFrame()

    df['Temperatures'] = country_temp
    df['C02 Levels'] = country_co2
    df['Years'] = df.index

    # Modifying data to make plotting easier:
    #       It merges the data into one column, and adds a column to match the
    #       temp data and the C02 data

    df = df.melt(id_vars='Years', value_vars=['Temperatures', 'C02 Levels'])
    df = df.rename(columns={'variable': 'Variables', 'value': 'Temps/C02 Levels'})
    fig = px.line(df, x='Years', y='Temps/C02 Levels', color='Variables')

 
    return fig

def world_map(df, year):
    # create the map !
    # locations = alpha 3 code for each country
    fig = px.choropleth(df, locations=df.index, color=year,
                        color_continuous_scale='RdYlGn_r', template="plotly_dark",
                       title='World Temperature ' + year)
    
    # set the mapbox (several possibilities)
    # set the zoom when the graph is displayed
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=1)
    # center title and set margin
    fig.update_layout(title_x=0.5, margin={"r":0, "t":30,"l":0,"b":0})
#     fig.update_layout(
#             updatemenus=[
#                 # item list = list of the charts !
#                 dict(buttons=list(item_list),  

#                  # place of the dropdown menu
#                 direction="down",showactive=True,x=0.005,
#                 xanchor="left",y=1.4,yanchor="top") ] )
    fig.show()

def temp_vs_co2(temp_df, co2_df, country_codes):
    '''
        temp_vs_co2: creates all temperature versus C02 graphs, with a drop down menu of the country name
    '''
    fig = go.Figure()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    buttons = []

    for i,country in enumerate(country_codes):
        
        fig.add_trace(create_co2_temp_fig(temp_df, co2_df,country)['data'][0], secondary_y=False)
        fig.add_trace(create_co2_temp_fig(temp_df, co2_df,country)['data'][1], secondary_y=True)
        
        # 2 Graphs per country
        args = [False] * len(country_codes)*2
        if i != len(country_codes) - 1:
            args[i] = True
            args[i+1] = True
        button = dict(label = country,
                    method = "update",
                    args=[{"visible": args}])
        
        #add the button to our list of buttons
        buttons.append(button)


    fig.update_layout(
        updatemenus=[
            dict(
            #change this to "buttons" for individual buttons
            type="dropdown",
            #this can be "left" or "right" as you like
            direction="down",
            #(1,1) refers to the top right corner of the plot
            x = 1,
            y = 1,
            #the list of buttons we created earlier
            buttons = buttons)
        ],
        title="Temperature VS. C02 Levels",
        title_x=0.5,
        xaxis_title="Years",
        legend_title="Plots",
        #so the x axis increments once per year
        xaxis = dict(dtick = 1))


        
    fig.update_yaxes(title_text="Temperature Data", secondary_y=False)
    fig.update_yaxes(title_text="C02 Levels", secondary_y=True)

    fig.show()

def find_correl(df1, df2):
    '''
        find_correl: Finds the correlation between two data frames, and returns a dataframe of 
                     the correlations
    '''
    correl_df = pd.DataFrame(index=df1.index)
    correls = []

    for i in df1.index:
        a_df = df1.loc[i]
        b_df = pd.to_numeric(df2.loc[i],errors = 'coerce')
        correls.append(a_df.corr(b_df))

    correl_df['Corr'] = correls
    # correl_df = correl_df.reset_index()

    return correl_df

def add_countries(df):
    country_names = []
    for i in df.index:
        country_names.append(pycountry.countries.get(alpha_3=i).name)
    df['Country'] = country_names
    return df

year_labels = create_year_labels(list(range(1901, 2022)))
country_codes, country_names = get_countries('data/temp/')
temp_df = merge_data('data/temp/tas_timeseries_annual_cru_1901-2021_', country_codes, country_names,year_labels)

co2_df = format_co2_data('data/co2/co2_data.csv')

temp_df,co2_df = match_data(temp_df, co2_df)

country_codes = temp_df.index

# world_map(temp_df, '1997 [YR1997]') 
# temp_vs_co2(temp_df, co2_df, country_codes)

df_correl = find_correl(temp_df, co2_df)
df_correl = add_countries(df_correl)

fig = px.scatter(df_correl, x= range(len(df_correl.index)),y='Corr', color = 'Country')
fig.update_layout(
        title="Temperature VS. C02 Correlation",
        title_x=0.5,
        yaxis_title="Correlation")

st.plotly_chart(fig)
#fig.show()


df_avg = pd.DataFrame(columns=['Average Temp Delta','Average C02 Delta'])
first_year = temp_df.columns[0]
last_year = temp_df.columns[-1]

delta=temp_df[last_year] - temp_df[first_year]

df_avg['Average Temp Delta'] = (delta.div(len(temp_df.columns)))

co2_yo = pd.to_numeric(co2_df[first_year],errors = 'coerce')
co2_yl = pd.to_numeric(co2_df[last_year],errors = 'coerce')
df_avg['Average C02 Delta'] = ((co2_yl - co2_yo).div(len(co2_df.columns)))

df_avg = add_countries(df_avg)

df_avg['co2_vs_temp'] = df_avg['Average C02 Delta']/df_avg['Average Temp Delta']
fig = px.scatter(df_avg, x="Average Temp Delta", y="Average C02 Delta", color='Country')
fig.update_layout(
        title="Temperature Change VS. C02 Change",
        title_x=0.5)
st.plotly_chart(fig)
#fig.show()