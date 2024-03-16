
import streamlit as st
import pandas as pd

def load_data():
    locations_df = pd.read_excel('Locations_Belgium_Updated.xlsx')
    weather_data_df = pd.read_excel('Weather_Data_Belgium_Updated.xlsx')
    return locations_df, weather_data_df

locations_df, weather_data_df = load_data()

st.title('Weather Monitoring in Belgium')

selected_location = st.selectbox('Select a location:', locations_df['location_name'].unique())

if selected_location:
    location_id = locations_df.loc[locations_df['location_name'] == selected_location, 'location_id'].iloc[0]
    selected_weather_data = weather_data_df[weather_data_df['location_id'] == location_id]
    latest_weather_data = selected_weather_data.sort_values(by='timestamp', ascending=False).head(1)
    
    if not latest_weather_data.empty:
        st.write(f"Weather conditions for {selected_location}:")
        st.write(latest_weather_data)
    else:
        st.write("No weather data available for the selected location.")
