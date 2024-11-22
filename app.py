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
json_file_path = 'data.json'

regiones_map = {
                2: "Región de Tarapacá",
                3: "Región de Antofagasta",
                4: "Región de Atacama",
                5: "Región de Coquimbo",
                6: "Región de Valparaíso",
                7: "Región Metropolitana del Gran Santiago",
                8: "Región de O'Higgins",
                9: "Región del Maule",
                10: "Región del Biobío",
                11: "Región de la Araucanía",
                12: "Región de Los Ríos",
                13: "Región de Los Lagos",
                14: "Región de Aysén",
                16: "Región de Ñuble"
            }

def obtenerDatos():
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Cargar los datos del archivo JSON
            # Diccionario de mapeo de FK a nombres de región (puedes ajustarlo según tus datos)
            # Reemplazar FK con nombres de región
            for item in data:
                if 'fk_region' in item:
                    # Reemplazar el número de la región con el nombre correspondiente
                    item['region_nombre'] = regiones_map.get(item['fk_region'], f"Región {item['fk_region']}")
            
            st.write("Datos cargados correctamente.")
            return pd.DataFrame(data)  # Convertir los datos a un DataFrame de Pandas
    except Exception as e:
        st.error(f"Error al cargar el archivo JSON: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

st.set_page_config(page_title="Farmacias Chile", page_icon=":flag_chile:", layout="wide")

# Cargar CSS desde la carpeta 'style'
def cargar_estilos():
    with open("style/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Llamar a la función para cargar los estilos
cargar_estilos()

# Cargar datos
datos = obtenerDatos()

#intro

with st.container():
    st.title('Análisis y Visualización de Farmacias en Chile')
    st.write('Esta aplicación web permite visualizar la ubicación de las farmacias en Chile, además de información relevante sobre ellas.')

# Crear contenedor para filtros y resultados
if not datos.empty:

    # Crear columnas para sidebar y contenido principal
    col_filtros, col_contenido = st.columns([1, 16])

    # Crear columnas para sidebar y contenido principal
col_filtros, col_contenido = st.columns([1, 16])

with col_filtros:
    # Filtros en la columna izquierda
    st.sidebar.header("Filtros de Búsqueda")

    # Filtro de Región con Checkboxes
    st.sidebar.subheader("Regiones")
    regiones = datos["region_nombre"].unique()
    selected_regiones = st.sidebar.multiselect(
        "Selecciona y busca por Regiones",
        options=regiones,  # Lista de regiones
        default=[]
    )

    # Filtro de Localidad con Checkboxes
    st.sidebar.subheader("Localidades")
    if selected_regiones:  # Mostrar solo localidades dentro de las regiones seleccionadas
        localidades = datos[datos["region_nombre"].isin(selected_regiones)]["localidad_nombre"].unique()
    else:
        localidades = datos["localidad_nombre"].unique()  # Todas las localidades

    selected_localidades = st.sidebar.multiselect(
        "Selecciona y busca por Localidades",
        options=localidades,
        default=[]
    )

    # Filtro de Comuna con Checkboxes
    st.sidebar.subheader("Comunas")
    if selected_localidades:  # Mostrar solo comunas dentro de las localidades seleccionadas
        comunas = datos[datos["localidad_nombre"].isin(selected_localidades)]["comuna_nombre"].unique()
    elif selected_regiones:  # Mostrar comunas dentro de las regiones seleccionadas
        comunas = datos[datos["region_nombre"].isin(selected_regiones)]["comuna_nombre"].unique()
    else:
        comunas = datos["comuna_nombre"].unique()  # Todas las comunas

    selected_comunas = st.sidebar.multiselect(
        "Selecciona y busca por Comunas",
        options=comunas,
        default=[]
    )

# Aplicar filtros al DataFrame
datos_filtrados = datos.copy()

if selected_regiones:  # Filtrar por regiones seleccionadas
    datos_filtrados = datos_filtrados[datos_filtrados["region_nombre"].isin(selected_regiones)]

if selected_localidades:  # Filtrar por localidades seleccionadas
    datos_filtrados = datos_filtrados[datos_filtrados["localidad_nombre"].isin(selected_localidades)]

if selected_comunas:  # Filtrar por comunas seleccionadas
    datos_filtrados = datos_filtrados[datos_filtrados["comuna_nombre"].isin(selected_comunas)]

# Mostrar datos filtrados
with col_contenido:
    st.subheader("Datos de Farmacias Filtrados")
    st.dataframe(datos_filtrados)

# Gráfico de cantidad de farmacias basado en filtros
if not datos_filtrados.empty:
    st.subheader("Gráfico: Cantidad de Farmacias Filtradas")

    # Determinar el campo de agrupación dinámicamente según los filtros aplicados
    if selected_comunas:
        agrupacion = "comuna_nombre"
        titulo_grafico = "Comunas"
    elif selected_localidades:
        agrupacion = "localidad_nombre"
        titulo_grafico = "Localidades"
    elif selected_regiones:
        agrupacion = "region_nombre"
        titulo_grafico = "Regiones"
    else:
        agrupacion = "region_nombre"
        titulo_grafico = "Regiones (sin filtros aplicados)"

    # Contar ocurrencias en la columna de agrupación
    grafico_datos = datos_filtrados[agrupacion].value_counts()

    # Crear el gráfico solo si hay datos
    if not grafico_datos.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        grafico_datos.plot(kind="bar", ax=ax, color="#4CAF50")
        ax.set_title(f"Cantidad de Farmacias por {titulo_grafico}")
        ax.set_xlabel(titulo_grafico)
        ax.set_ylabel("Cantidad")
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        st.pyplot(fig)
    else:
        st.write("No hay datos suficientes para generar el gráfico.")

    # Descargar datos filtrados
    if not datos_filtrados.empty:
        st.download_button(
            label="Descargar datos filtrados en CSV",
            data=datos_filtrados.to_csv(index=False),
            file_name="farmacias_filtradas.csv",
            mime="text/csv"
        )