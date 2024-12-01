import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Análisis Estadístico",
    page_icon="📊",
    layout="wide"
)

# Función para cargar datos
@st.cache_data
def cargar_datos():
    ruta_base = Path(__file__).parent.parent
    ruta_datos = ruta_base / 'data' / 'encuesta_recreacion.csv'
    return pd.read_csv(ruta_datos)

# Cargar datos
df = cargar_datos()

# Título principal
st.title("📊 Análisis de Encuesta de Recreación")

# Selector de variable a analizar
variable_seleccionada = st.selectbox(
    "Seleccione la variable a analizar",
    ["Edad", "Género", "Ubicación del Centro", "Frecuencia de Visitas", 
     "Actividades", "Compañía", "Residencia", "Preferencia", 
     "Época del Año de Visita Frecuente", "Importancia del Costo de Entrada", "Satisfacción"]
)

# Selector de tipo de gráfico
tipo_grafico = st.radio(
    "Seleccione tipo de gráfico",
    ["Gráfico de Barras", "Gráfico Circular"]
)

# Preparar datos
counts = df[variable_seleccionada].value_counts().reset_index()
counts.columns = ['Categoría', 'Cantidad']

# Crear gráfico
if tipo_grafico == "Gráfico de Barras":
    fig = px.bar(
        counts,
        x='Categoría',
        y='Cantidad',
        title=f'Distribución de {variable_seleccionada}',
        labels={'Categoría': variable_seleccionada}
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500
    )
else:  # Gráfico Circular
    fig = px.pie(
        counts,
        values='Cantidad',
        names='Categoría',
        title=f'Distribución de {variable_seleccionada}'
    )
    fig.update_layout(height=500)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

# Mostrar datos
st.subheader("Tabla de Frecuencias")
st.dataframe(counts.style.bar(subset=['Cantidad'], color='#5fba7d'))
