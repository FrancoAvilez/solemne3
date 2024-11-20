import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

url="https://midas.minsal.cl/farmacia_v2/WS/getLocales.php"

# def obtenerDatos():
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return pd.DataFrame(response.json())
#     else:
#         st.error("Error al obtener datos de la API.")
#         return pd.DataFrame()  # Devuelve un DataFrame vacío si falla
response = requests.get(url)
data = response.json()
datos = pd.DataFrame(data)

st.set_page_config(page_title="Farmacias Chile", page_icon=":flag_chile:", layout="wide")

#intro

with st.container():
    st.header('Datos Oficiales')
    st.title('Análisis y Visualización de Farmacias en Chile')
    st.write('Esta aplicación web permite visualizar la ubicación de las farmacias en Chile, además de información relevante sobre ellas.')


# Cargar datos
#datos = obtenerDatos()

if not datos.empty:
    # Mostrar tabla
    st.subheader("Datos de Farmacias")
    st.dataframe(datos)
else:
    st.warning("No se pudieron cargar los datos.")

if not datos.empty:
    # Crear filtro por comuna
    comunas = datos["comuna"].unique()
    comuna_seleccionada = st.selectbox("Selecciona una comuna", options=comunas)

    # Filtrar datos
    datos_filtrados = datos[datos["comuna"] == comuna_seleccionada]

    # Mostrar datos filtrados
    st.write(f"Farmacias en {comuna_seleccionada}:")
    st.dataframe(datos_filtrados)

if not datos_filtrados.empty:
    # Crear un gráfico de barras con la cantidad de farmacias por comuna
    st.subheader("Gráfico: Cantidad de Farmacias por Comuna")

    # Datos para el gráfico
    grafico_datos = datos_filtrados["comuna"].value_counts()

    # Crear el gráfico
    fig, ax = plt.subplots()
    grafico_datos.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_title("Cantidad de Farmacias por Comuna")
    ax.set_xlabel("Comuna")
    ax.set_ylabel("Cantidad")

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

if not datos_filtrados.empty:
    # Descargar datos filtrados
    st.download_button(
        label="Descargar datos filtrados en CSV",
        data=datos_filtrados.to_csv(index=False),
        file_name="farmacias_filtradas.csv",
        mime="text/csv"
    )
