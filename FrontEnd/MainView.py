import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
st.set_page_config(page_title="MONAQ", page_icon="📈")
st.title("MONAQ")

def SensorCard(sensor_id,sensor,st):
    """
    Renders a card with information about a sensor.

    Args:
        sensor_id (int): The ID of the sensor.
        sensor (dict): A dictionary containing the sensor's temperature, humidity, and CO2 values.
        st (Streamlit): The Streamlit object used to render the card.

    Returns:
        None
"""
    if 400 <= sensor["co2"] <= 1000:
        status = "V pořádku"
    elif 1000 <= sensor["co2"] < 2000:
        status = "Vydýcháno"
    elif sensor["co2"] > 2000:
        status = "Špatná, Otevřte Okna"
    # source: https://www.co2meter.com/blogs/news/carbon-dioxide-indoor-levels-chart
    with st.container(border=True):
        st.header(f"Senzor: {sensor_id}")
        st.text(f"Status: {status}")
        st.text(f"Teplota: {sensor['temperature']} °C")  
        st.text(f"Vlhkost: {sensor['humidity']} %")  
        st.text(f"CO2: {sensor['co2']} ppm")  
        st.link_button("Otevřít",url=f"http://localhost/SensorView?id={sensor_id}", use_container_width=True)

try:
   
    # Get all sensors from database/api
    try:
        data = requests.get("http://fastapi:8085/getAllSensors")
        data_json = data.json()
        df_raw = pd.DataFrame().from_dict(data_json["sensors"])
    except:
        # If there is an error return empty dataframe
        st.error("Nastala chyba")
        df_raw = pd.DataFrame()
    # Convert records to dataframe

    df_raw.set_index("sensor_id",inplace=True)
    # Convert timestamp to datetime
    df_raw["updated_at"] = pd.to_datetime(df_raw["updated_at"])
    # Sort by timestamp
    sorted_df = df_raw.sort_values(by=['updated_at'],ascending=False)
    
    # Convert lat and long to float
    sorted_df["loc_lat"] = sorted_df["loc_lat"].astype(float)
    sorted_df["loc_long"] = sorted_df["loc_long"].astype(float)
    sorted_df["static_size"] = 0.05

    unique_sorted_records = sorted_df.drop_duplicates(subset=['loc_lat', 'loc_long'], keep='last')
    
    px.set_mapbox_access_token(os.getenv("MAPBOX_TOKEN"))
    fig = px.scatter_mapbox(unique_sorted_records, lat="loc_lat", lon="loc_long", color="co2",color_continuous_scale=px.colors.cyclical.IceFire,zoom=2)

    st.divider()
    st.header("Vizualizace geodat")
    st.plotly_chart(fig)
    st.divider()
    st.title("Senzory")
    num_columns = 3
    total_records = len(sorted_df)
    ideal_records_per_col = total_records // num_columns
    extra_records_cols = total_records % num_columns

    L, M, R = st.columns([5, 5, 5])


    column_index = 0
    for index, row in sorted_df.iterrows():
        if column_index < extra_records_cols:
            with (L if column_index == 0 else M if column_index == 1 else R):
                SensorCard(index,row,st)
        else:
            with (L if column_index % num_columns == 0 else M if column_index % num_columns == 1 else R):
                SensorCard(index,row,st)
        column_index += 1
        if column_index == num_columns:
            column_index = 0

except Exception as e:
    st.write("error",e)