import numpy as np
import pandas as pd
import country_converter as coco
import streamlit as st

@st.cache
def get_data():
    df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

    # take usefull columns
    df = df[['location', 'date','people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred', 'new_cases_per_million']]

    # drop continents
    drop_continents = ['Africa', 'Asia', 'Europe', 'South America', 'North America', 'European Union', 'World', 'International', 'Oceania']
    df = df[~df['location'].isin(drop_continents)]

    # fill missing values with 0
    df = df.fillna(0)

    # replace 0 with previous nonzero value
    df_copy = df.copy()
    df.drop(df.index, inplace=True)
    for loc in df_copy.location.unique():
        temp = df_copy[df_copy.location==loc]
        temp['people_fully_vaccinated_per_hundred'] = temp['people_fully_vaccinated_per_hundred'].replace(to_replace=0, method='ffill')
        temp['people_vaccinated_per_hundred'] = temp['people_vaccinated_per_hundred'].replace(to_replace=0, method='ffill')
        df = pd.concat([df,temp])

    # create column with iso number of country
    df['iso'] = np.nan
    df.iso = coco.convert(names=df.location, to='ISO3', not_found='TLS')

    return df