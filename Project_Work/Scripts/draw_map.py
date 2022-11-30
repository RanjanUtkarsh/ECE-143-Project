import plotly.express as px
import streamlit as st


def world_map(df, year, title):
    """
    This method is to draw a heat map in a world map for a specific aspect and year.
    :param df: dataframe
    :param year: a specific year
    :param title: an aspect
    :return: a heat map in a world map
    """
    # create the map !
    # locations = alpha 3 code for each country
    color = 'YlGn'
    target = title
    if title == 'co2':
        title = "CO2 Emission in "
        color = 'RdYlGn_r'
    elif title == 'eco_freedom':
        title = "Economic Freedom in "
    elif title == 'politic regime':
        title = "Politic regime of each country in "
        target = 'regime_row_owid'
    else:
        raise ValueError("Sorry, there is no data about {} in {}".format(title, year))

    fig = px.choropleth(df, locations=df['Code'], color=target,
                        color_continuous_scale=color, template="plotly_dark",
                        title=title + year)

    # set the mapbox (several possibilities)
    # set the zoom when the graph is displayed
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=1)
    # center title and set margin
    fig.update_layout(title_x=0.5, margin={"r": 0, "t": 30, "l": 0, "b": 0})
    return st.plotly_chart(fig)


def plot(df, yr, title):
    """
    This method is to preprocess the dataframe
    :param df: a dataframe
    :param yr: a year
    :param title: an aspect
    :return: calling the function world_map to display a map
    """
    yr = str(yr)
    years = sorted(set(df['year']))
    assert int(yr) in years, "Please provide a year from {} and {}".format(years[0], years[-1])
    final_yr = yr + ' ' + '[YR' + yr + ']'
    df = df[df.year == int(yr)]
    return world_map(df, final_yr, title)