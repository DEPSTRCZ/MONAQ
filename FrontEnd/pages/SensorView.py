import streamlit as st
import requests as rq
import pandas as pd
import pytz
from datetime import datetime

# Get query params
if "id" in st.query_params:
    query_sensor_id = st.query_params["id"]
else:
    st.error("Nebyl vybrán žádný senzor.")
    st.stop()

# Get sensor data from API
try:
    response = rq.get(f"http://fastapi:8085/getSensor/{query_sensor_id}")
    data = response.json()
    df = pd.DataFrame().from_dict(data.get("records"))
except:
    st.error("Nastala chyba")
    df = pd.DataFrame()


# Convert df to datetime
df["updated_at"] = pd.to_datetime(df["updated_at"])

# Convert to local time
local_tz = pytz.timezone("Europe/Prague")
df['local_updated_at'] = df.apply(
    lambda row: row['updated_at'].tz_localize(pytz.utc).astimezone(local_tz)
    if pd.notnull(row['updated_at']) else None, axis=1
)
# Parse to float
df[["humidity", "loc_lat", "loc_long", "temperature",]] = df[["humidity", "loc_lat", "loc_long", "temperature",]].astype(float)
# Sort values
df = df.sort_values(by="updated_at", ascending=False)


# Get deltas
try:
    response_quality = rq.get(f"http://fastapi:8085/getQualityInfo/{query_sensor_id}")
    data_quality = response_quality.json()
except:
    st.error("Nastala chyba při náčítání dat")
    st.stop()

# Asign deltas and values for each metric.



st.title(f"Senzor: {query_sensor_id}")

# Convert UTC timestamp to local time
timestamp = datetime.strptime(data["last_update"], "%Y-%m-%dT%H:%M:%S")
parsed_utc = timestamp.replace(tzinfo=pytz.utc)
timestamp_formatted = parsed_utc.astimezone(local_tz).strftime("%d.%m.%Y %H:%M:%S")



st.markdown(f"### Poslední aktualizace {timestamp_formatted}")
st.divider()

L, M, R = st.columns([2.2,5,2.2])
#humid and temp is an object thats supposed to be the humidity and Temperature of the sensor.
with L:
    with st.container(border=True):
        st.metric(label="Vlhkost", value=f"{data_quality['humidity']} %", delta=f"{data_quality['delta_humidity']} %", delta_color="inverse")

with M:
    with st.container(border=True):

        if 400 <= data_quality["co2"] <= 1000:
            status = "V pořádku"
            st.image("https://wallpapercave.com/wp/c0slfXe.jpg")
        elif 1000 <= data_quality["co2"] < 2000:
            status = "Vydýcháno"
            st.image("https://positivebloom.com/wp-content/uploads/2022/08/The-rose-flower-is-dried-by-the-hot-summer-sun.jpg.webp")
        elif data_quality["co2"] > 2000:
            status = "Špatná, Otevřte Okna"
            st.image("http://1.bp.blogspot.com/-CWfbSG_cb_g/TcqHVdw7aRI/AAAAAAAAAPo/hSB0-ad4068/s1600/Dead+roseB.jpg")

        with st.container(border=True):
            st.metric(label="CO₂", value=f"{data_quality['co2']} ppm", delta=f"{data_quality['delta_co2']} ppm", delta_color="inverse")
        with st.container(border=True):
            st.subheader(f"Status: {status}")

with R:
    with st.container(border=True):
        st.metric(label="Teplota", value=f"{data_quality['temperature']} °C", delta=f"{data_quality['delta_temperature']} °C")
# note: 400-1000 ppm = ok co2 lvls. | 1000+ ppm is bad
st.title("Grafy")
st.divider()

# Graphs of temperature, humidity and CO2
st.header("Teplota", divider="orange")
st.line_chart(df, x="local_updated_at", y="temperature", color="#FFA500")    #temperature
st.header("Vlhkost", divider="blue")
st.line_chart(df, x="local_updated_at", y="humidity", color="#006FAF")    #humidity
st.header("CO₂", divider="grey")
st.line_chart(df, x="local_updated_at", y="co2", color="#90999F")    #CO2