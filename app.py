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

def obtenerDatos():
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Cargar los datos del archivo JSON
            # Transformación de foreign keys a nombres de región
            # Diccionario de mapeo de FK a nombres de región (puedes ajustarlo según tus datos)
            regiones_map = {
                1: "Región de Tarapacá",
                2: "Región de Antofagasta",
                3: "Región de Atacama",
                4: "Región de Coquimbo",
                5: "Región de Valparaíso",
                6: "Región del Libertador General Bernardo O'Higgins",
                7: "Región del Maule",
                8: "Región del Biobío",
                9: "Región de la Araucanía",
                10: "Región de Los Lagos",
                11: "Región de Aysén del General Carlos Ibáñez del Campo",
                12: "Región de Magallanes y de la Antártica Chilena",
                13: "Región Metropolitana de Santiago",
                14: "Región de Los Ríos",
                15: "Región de Arica y Parinacota",
                16: "Región de Ñuble"
            }
            
            # Reemplazar FK con nombres de región
            for item in data:
                if 'fk_region' in item:
                    item['region_nombre'] = regiones_map.get(item['fk_region'], f"Región {item['fk_region']}")
            st.write("Datos cargados correctamente.")
            return pd.DataFrame(data)  # Convertir los datos a un DataFrame de Pandass
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
    st.header('Datos Oficiales')
    st.title('Análisis y Visualización de Farmacias en Chile')
    st.write('Esta aplicación web permite visualizar la ubicación de las farmacias en Chile, además de información relevante sobre ellas.')

# Crear contenedor para filtros y resultados
if not datos.empty:

    # Crear columnas para sidebar y contenido principal
    col_filtros, col_contenido = st.columns([1, 16])

    with col_filtros:
        # Filtros en la columna izquierda
        st.sidebar.header("Filtros de Búsqueda")

 
        texto_farmacia = st.sidebar.text_input("Buscar farmacia por nombre", "")

        # Filtro de Región con Checkboxes
        st.sidebar.subheader("Regiones")
        regiones = datos["region_nombre"].unique()
        selected_regiones = st.sidebar.multiselect(
            "Selecciona y busca por Regiones",
            options=["--"] + list(regiones),  # Agregar opción "--"
            default=["--"]  # Opción por defecto
        )

        # Filtro de Localidad con Checkboxes
        st.sidebar.subheader("Localidades")
        if selected_regiones and "--" not in selected_regiones:
            localidades = datos[datos["region_nombre"].isin(selected_regiones)]["localidad_nombre"].unique()
        else:
            localidades = datos["localidad_nombre"].unique()

        selected_localidades = st.sidebar.multiselect(
            "Selecciona Localidades",
            options=["--"] + list(localidades),  # Agregar opción "--"
            default=["--"]  # Opción por defecto
        )

    with col_contenido:
        # Aplicar filtros solo si no se selecciona la opción "--"
        datos_filtrados = datos.copy()

        if texto_farmacia:
            datos_filtrados = datos_filtrados[datos_filtrados["local_nombre"].str.contains(texto_farmacia, case=False, na=False)]

        if selected_regiones and "--" not in selected_regiones:
            datos_filtrados = datos_filtrados[datos_filtrados["region_nombre"].isin(selected_regiones)]

        if selected_localidades and "--" not in selected_localidades:
            datos_filtrados = datos_filtrados[datos_filtrados["localidad_nombre"].isin(selected_localidades)]

        # Mostrar datos filtrados
        st.subheader("Datos de Farmacias")
        
        tab1, tab2 = st.tabs(["Todos los Datos", "Datos Filtrados"])
        
        with tab1:
            st.dataframe(datos)
        
        with tab2:
            st.dataframe(datos_filtrados)

    # Gráfico de cantidad de farmacias
    if not datos_filtrados.empty:
        st.subheader("Gráfico: Cantidad de Farmacias")
        
        opcion_grafico = st.selectbox("Agrupar por:", ["--"] + ["Región", "Localidad", "Comuna"])  # Agregar opción "--"
        
        if opcion_grafico == "Región":
            grafico_datos = datos_filtrados["region_nombre"].value_counts()
        
        elif opcion_grafico == "Localidad":
            grafico_datos = datos_filtrados["localidad_nombre"].value_counts()
        
        else:
            grafico_datos = pd.Series()  # Si se selecciona "--", no se muestra gráfico

        if not grafico_datos.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            grafico_datos.plot(kind="bar", ax=ax, color="skyblue")
            ax.set_title(f"Cantidad de Farmacias por {opcion_grafico}")
            ax.set_xlabel(opcion_grafico)
            ax.set_ylabel("Cantidad")
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            st.pyplot(fig)

    # Descargar datos filtrados
    if not datos_filtrados.empty:
        st.download_button(
            label="Descargar datos filtrados en CSV",
            data=datos_filtrados.to_csv(index=False),
            file_name="farmacias_filtradas.csv",
            mime="text/csv"
        )