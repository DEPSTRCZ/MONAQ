import streamlit as st
st.set_page_config(page_title="MONAQ", page_icon="📈")
st.title("MONAQ")
st.header("Vizualizace kvality vzduchu.")
st.divider()
st.info("Momentálně není vybrán žádný senzor")


left, mid, right = st.columns([5, 10, 5],gap="small")
with st.sidebar:
    st.title("Vyberte senzor")
    for id in range(10):
        container = st.container(border=True)
        container.header(f"Senzor {id}")
        container.button("Zobrazit",key=id)
with left:
    st.write()

with mid:
    st.write()

with right:
    st.write()