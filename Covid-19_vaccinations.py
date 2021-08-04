import streamlit as st
import pandas as pd
import datetime as dt
import plotly.express as px
from prepare_data import get_data

df = get_data()

st.markdown("""
# Covid-19 vacciantions visualization
""")

# add date selector
date_format = 'MMM DD, YYYY'
start_date = dt.date(year=2020, month=12, day=1)
end_date = pd.to_datetime(df.date.max()).date()
date = st.slider('Select date', min_value=start_date, value=end_date , max_value=end_date, format=date_format)

# add choropleth map
fig = px.choropleth(df[df.date==str(date)], 
                    locations='iso',
                    color='people_fully_vaccinated_per_hundred',
                    hover_name='location',
                    hover_data = {'iso': False, 'people_fully_vaccinated_per_hundred': True},
                    title=f'Percentage of people fully vaccinated on {date}',
                    labels={'people_fully_vaccinated_per_hundred': '%'})
st.plotly_chart(fig)

# add country selector
countries = st.multiselect('Pick countries', sorted(df.location.unique()), 'Poland')

# add table
rename = {'people_vaccinated_per_hundred': 'vaccinated [%]',
          'people_fully_vaccinated_per_hundred': 'fully vaccinated [%]',
          'new_cases_per_million': 'cases per million'}
st.write(df[(df.location.isin(countries)) & (df.date==str(date))].set_index('location').drop(columns=['date', 'iso']).rename(columns=rename))