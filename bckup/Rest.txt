def senzor(rkey):
    st.title("SENSOR X")
    st.text("Status: #")  
    st.text("Temperature: #")  
    st.text("Moisture: #")  
    st.text("C02: #")  
    st.text("Quality: #")  
    st.text("Time: D.M.Y - H:M:S")
    st.button("Inspect",key=rkey, help="Inspect the sensor data.", use_container_width=True)


L, M, R = st.columns([5,5,5])
GBJ = st.container(border=True)
# GBJ = Gay Baby Jail
with L:
    with st.container(border=True):
        senzor(1)

    with st.container(border=True):
        senzor(2)

with M:
    with st.container(border=True):
        senzor(3)
    with st.container(border=True):
        senzor(4)
        
with R:
    with st.container(border=True):
        senzor(5)
    with st.container(border=True):
        senzor(6)