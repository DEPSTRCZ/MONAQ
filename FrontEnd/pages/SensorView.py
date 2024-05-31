import streamlit as st
import plotly.express as px
import requests as rq
import pandas as pd

sensor = "Sensor: 0"




st.markdown(sensor)
st.sidebar.markdown(sensor)
try:
    st.write(st.query_params)
    st.write("id" in st.query_params)
    if "id" in st.query_params:
        query_sensor_id = st.query_params["id"]
    else:
        st.error("Nebyl vybrán žádný senzor.")
        st.stop()
    st.write(query_sensor_id)
    responce = rq.get(f"http://fastapi:8085/getSensor/{query_sensor_id}")
    st.write(responce.content)
    data = responce.json()
    df = pd.DataFrame().from_dict(data)
    df = df["records"].apply(pd.Series)
    st.write(df)
except Exception as e:
    st.write(e)

SoTD = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
# SoTD = Screams Of The Damned
st.header(" ", divider="rainbow")

deltaH = 10

L, M, R = st.columns([2,5,2])
#humid and temp is an object thats supposed to be the humidity and Temperature of the sensor.
with L:
    with st.container(border=True):
        st.metric(label="Humidity", value=df["humidity"], delta="-50 %")

with M:
    with st.container(border=True):
        st.image("https://i.pinimg.com/736x/b3/1e/e3/b31ee3988b009d32478769af874f8a4d.jpg")
        with st.container(border=True):
            st.metric(label="CO₂", value="5'000 ppm", delta="+4'000 ppm", delta_color="inverse")
        with st.container(border=True):
            st.subheader("Status: 'LORD OF CINDER'")
        st.button(label="Inspect", key=1)

with R:
    with st.container(border=True):
        st.metric(label="Temperature", value="200 °C", delta="4 °C")
# note: 400-1000 ppm = ok co2 lvls. | 1000+ ppm is bad
