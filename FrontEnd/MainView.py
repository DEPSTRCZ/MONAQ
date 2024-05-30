import streamlit as st
import requests
import pandas as pd
st.set_page_config(page_title="MONAQ", page_icon="📈")
st.title("MONAQ")
st.header("Vizualizace kvality vzduchu.")
st.divider()
st.info("Momentálně není vybrán žádný senzor")
st.write("cs2")

try:
    st.write("http://fastapi:80/GetAllSensors")
    data = requests.get("http://fastapi:8085/getAllSensors")
    
    st.write(data.content)
    df = pd.read_json(data)
    st.dataframe(df)

except Exception as e:
    st.write("error",e)