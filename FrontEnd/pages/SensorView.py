import streamlit as st
import requests as rq
import pandas as pd
import pytz
# Get query params
if "id" in st.query_params:
    query_sensor_id = st.query_params["id"]
else:
    st.error("Nebyl vybrán žádný senzor.")
    st.stop()

try:
    responce = rq.get(f"http://fastapi:8085/getSensor/{query_sensor_id}")
    data = responce.json()
    df = pd.DataFrame().from_dict(data)
except:
    st.error("Nastala chyba")
    df = pd.DataFrame()

df = df["records"].apply(pd.Series)
df["updated_at"] = pd.to_datetime(df["updated_at"])
df[["humidity", "loc_lat", "loc_long", "temperature",]] = df[["humidity", "loc_lat", "loc_long", "temperature",]].astype(float)
df = df.sort_values(by="updated_at", ascending=False)

df_delta = df.head(2)
df_delta["delta_humidity"] = df_delta["humidity"].diff()
df_delta["delta_temperature"] = df_delta["temperature"].diff()
df_delta["delta_co2"] = df_delta["co2"].diff()
delta_humidity = round(df_delta['humidity'].iloc[-1] - df_delta['humidity'].shift(1).iloc[-1],2)
delta_temperature = round(df_delta['temperature'].iloc[-1] - df_delta['temperature'].shift(1).iloc[-1],2)
delta_co2 = df_delta['co2'].iloc[-1] - df_delta['co2'].shift(1).iloc[-1]


humidity = df_delta.iloc[-1]['humidity']
temperature = df_delta.iloc[-1]['temperature']
co2 = df_delta.iloc[-1]['co2']


st.title(f"Senzor: {query_sensor_id}")

# Convert UTC timestamp to local time
local_tz = pytz.timezone("Europe/Prague")
timestamp = df['updated_at'].iloc[-1].to_pydatetime()



st.markdown(f"### Poslední aktualizace {timestamp.strftime("%d.%m.%Y %H:%M:%S")}")
st.divider()

L, M, R = st.columns([2.2,5,2.2])
#humid and temp is an object thats supposed to be the humidity and Temperature of the sensor.
with L:
    with st.container(border=True):
        st.metric(label="Vlhkost", value=f"{humidity} %", delta=f"{delta_humidity} %", delta_color="inverse")

with M:
    with st.container(border=True):
        if humidity < 1000:
            st.image("https://wallpapercave.com/wp/c0slfXe.jpg")
        elif humidity < 1500:
            st.image("https://positivebloom.com/wp-content/uploads/2022/08/The-rose-flower-is-dried-by-the-hot-summer-sun.jpg.webp")
        else:
            st.image("http://1.bp.blogspot.com/-CWfbSG_cb_g/TcqHVdw7aRI/AAAAAAAAAPo/hSB0-ad4068/s1600/Dead+roseB.jpg")
        with st.container(border=True):
            st.metric(label="CO₂", value=f"{co2} ppm", delta=f"{delta_co2} ppm", delta_color="inverse")
        with st.container(border=True):
            if co2 < 1000:
                status = "V pořádku"
            elif co2 < 1500:
                status = "Vydýcháno"
            else:
                status = "Špatná, Otevřte Okna"
            st.subheader(f"Status: {status}")

with R:
    with st.container(border=True):
        st.metric(label="Teplota", value=f"{temperature} °C", delta=f"{delta_temperature} °C")
# note: 400-1000 ppm = ok co2 lvls. | 1000+ ppm is bad
st.title("Grafy")
st.divider()

# Graphs of temperature, humidity and CO2
st.header("Teplota", divider="orange")
st.line_chart(df, x="updated_at", y="temperature", color="#FFA500")    #temperature
st.header("Vlhkost", divider="blue")
st.line_chart(df, x="updated_at", y="humidity", color="#006FAF")    #humidity
st.header("CO₂", divider="grey")
st.line_chart(df, x="updated_at", y="co2", color="#90999F")    #CO2