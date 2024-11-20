import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
API="https://midas.minsal.cl/farmacia_v2/WS/getLocales.php"

# def obtenerDatos():
#     try:
#         response = requests.get(API)  # Realizar una solicitud GET a la API
#         # Mostrar el contenido de la respuesta
#         st.write("Respuesta:", response.text)  # Muestra el cuerpo de la respuesta
#         st.write("Código de estado:", response.status_code)  # Muestra el código de estado

#         # Asegúrate de que la respuesta tenga un código de estado 200
#         if response.status_code == 200:
#             data = response.json()  # Convirtiendo la respuesta JSON a un diccionario de Python
#             st.write("Datos obtenidos:", data)  # Muestra los datos obtenidos
#             return pd.DataFrame(data)  # Devuelve los datos como un DataFrame
#         else:
#             st.error("Error al obtener los datos. Código de estado: " + str(response.status_code))
#             return pd.DataFrame()  # Devuelve un DataFrame vacío si no se obtienen los datos

#     except Exception as e:
#         st.error(f"Ocurrió un error al intentar obtener los datos: {e}")
#         return pd.DataFrame()  # Devuelve un DataFrame vacío si hay un error

# Ruta al archivo JSON (asumimos que está en el mismo directorio que app.py)
json_file_path = 'datos.json'

def obtenerDatos():
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Cargar los datos del archivo JSON
            st.write("Datos cargados correctamente.")
            return pd.DataFrame(data)  # Convertir los datos a un DataFrame de Pandas
    except Exception as e:
        st.error(f"Error al cargar el archivo JSON: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

st.set_page_config(page_title="Farmacias Chile", page_icon=":flag_chile:", layout="wide")

# Cargar datos
datos = obtenerDatos()

#intro

with st.container():
    st.header('Datos Oficiales')
    st.title('Análisis y Visualización de Farmacias en Chile')
    st.write('Esta aplicación web permite visualizar la ubicación de las farmacias en Chile, además de información relevante sobre ellas.')

if not datos.empty:
    # Mostrar tabla
    st.subheader("Datos de Farmacias")
    st.dataframe(datos)
else:
    st.warning("No se pudieron cargar los datos.")

if not datos.empty:
    # Crear filtro por comuna
    comunas = datos["comuna_nombre"].unique()
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
