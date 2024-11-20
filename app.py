import streamlit as st
import pandas as pd
import requests

url="https://midas.minsal.cl/farmacia_v2/WS/getLocales.php"

response = requests.get(url)

data=response.json()

st.set_page_config(page_title="Farmacias Chile", page_icon=":shark:", layout="wide")

#intro

with st.container():
    st.header('Datos Oficiales')
    st.title('Farmacias Chile')
    st.write('Esta aplicación web permite visualizar la ubicación de las farmacias en Chile, además de información relevante sobre ellas.')
    