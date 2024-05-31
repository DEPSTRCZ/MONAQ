import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(page_title="MONAQ", page_icon="📈")
st.title("MONAQ")

def GetLatestRecordFromList(records):
    return records[-1]

try:
    data = requests.get("http://fastapi:8085/getAllSensors")
    
    data_json = data.json()
    df_raw = pd.DataFrame().from_dict(data_json)
    latest_records = df_raw["records"].apply(GetLatestRecordFromList)
    extracted = latest_records.apply(pd.Series)
    extracted.set_index("sensor_id",inplace=True)
    sorted_records = extracted.sort_values(by=['updated_at',"sensor_id"])
    
    sorted_records["loc_lat"] = sorted_records["loc_lat"].astype(float)
    sorted_records["loc_long"] = sorted_records["loc_long"].astype(float)
    sorted_records["static_size"] = 0.2

    unique_sorted_records = sorted_records.drop_duplicates(subset=['loc_lat', 'loc_long'], keep='last')
    

    
    px.set_mapbox_access_token(open(".mapbox").read())
    fig = px.scatter_mapbox(unique_sorted_records, lat="loc_lat", lon="loc_long", color="co2",color_continuous_scale=px.colors.cyclical.IceFire, size="static_size",zoom=2)

    st.divider()
    st.header("Vizualizace geodat")
    st.plotly_chart(fig)
    st.divider()
    st.title("Senzory")
    L, M, R = st.columns([5,5,5])
    st.write(sorted_records)
    for index, row in sorted_records.iterrows():  # Iterate over rows
        if index % 3 == 0:  # Place in left column (every 3rd row)
            with L:
                with st.container(border=True):
                    st.header(f"Senzor: {index}")  # Display specific columns
                    st.text(f"Teplota: {row['temperature']}")  # Display specific columns
                    st.text(f"Vlhkost: {row['humidity']}")  # Display specific columns
                    st.text(f"CO2: {row['co2']}")  # Display specific columns

        elif index % 3 == 1:  # Place in middle column (every 2nd row)
            with M:
                with st.container(border=True):
                    st.title(f"Senzor: {index}")  # Display specific columns
                    st.text(f"Teplota: {row['temperature']}")  # Display specific columns
                    st.text(f"Vlhkost: {row['humidity']}")  # Display specific columns
                    st.text(f"CO2: {row['co2']}")  # Display specific columns
        else:  # Place in right column (remaining rows)
            with R:
                with st.container(border=True):
                    st.title(f"Senzor: {index}")  # Display specific columns
                    st.text(f"Teplota: {row['temperature']}")  # Display specific columns
                    st.text(f"Vlhkost: {row['humidity']}")  # Display specific columns
                    st.text(f"CO2: {row['co2']}")  # Display specific columns
    

except Exception as e:
    st.write("error",e)