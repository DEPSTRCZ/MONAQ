import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(page_title="MONAQ", page_icon="📈")
st.title("MONAQ")

def GetLatestRecordFromList(records):
    return records[-1]

def SensorCard(sensor_id,sensor,st):
    with st.container(border=True):
        st.header(f"Senzor: {sensor_id}")  # Display specific columns
        st.text(f"Teplota: {sensor['temperature']}")  # Display specific columns
        st.text(f"Vlhkost: {sensor['humidity']}")  # Display specific columns
        st.text(f"CO2: {sensor['co2']}")  # Display specific columns
        st.button("Otevřít",key=sensor_id, use_container_width=True)

try:
    data = requests.get("http://fastapi:8085/getAllSensors")
    
    data_json = data.json()
    df_raw = pd.DataFrame().from_dict(data_json["sensors"])
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
    num_columns = 3
    total_records = len(sorted_records)
    ideal_records_per_col = total_records // num_columns
    extra_records_cols = total_records % num_columns

    L, M, R = st.columns([5, 5, 5])

    column_index = 0
    for index, row in sorted_records.iterrows():
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