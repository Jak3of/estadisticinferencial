import streamlit as st

st.set_page_config(
    page_title="Análisis Estadístico",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sistema de Análisis Estadístico")
st.markdown("""
### Bienvenido al Sistema de Análisis de Encuesta de Recreación

Este sistema te permite realizar diferentes tipos de análisis estadísticos sobre los datos de la encuesta de satisfacción del centro recreativo.

#### Secciones disponibles:

1. **📈 Análisis Descriptivo**
   - Visualización de variables
   - Gráficos de distribución
   - Tablas de frecuencia
   - Medidas de tendencia central y dispersión

2. **🔍 Análisis Inferencial**
   - Intervalos de Confianza:
     * Media (varianza conocida y desconocida)
     * Proporción
     * Diferencia de medias
     * Diferencia de proporciones
     * Varianza
   - Distribuciones Muestrales:
     * Media (varianza conocida y desconocida)
     * Proporción
     * Diferencia de medias
     * Diferencia de proporciones

3. **📊 Pruebas de Hipótesis**
   - Pruebas para la media
   - Pruebas para la proporción
   - Pruebas para diferencia de medias
   - Pruebas para diferencia de proporciones

4. **📈 Regresión**
   - Regresión lineal simple
   - Análisis de correlación
   - Visualización de tendencias

Selecciona una sección del menú lateral para comenzar tu análisis.

#### Características principales:
- Visualizaciones interactivas con Plotly
- Cálculos estadísticos precisos
- Interpretaciones automáticas de resultados
- Fórmulas matemáticas copiables en formato LaTeX
""")

# Información del dataset
st.sidebar.header("ℹ️ Información")
st.sidebar.markdown("""
- Total de encuestados: 30
- Variables analizadas: 11
- Última actualización: 2024
- Enfoque: Satisfacción del cliente
- Métricas clave: Género, Satisfacción, Frecuencia de visita
""")

# Agregar sección de integrantes
st.sidebar.header("👥 Integrantes")
st.sidebar.markdown("""
- Alfaro Muñoz, Anderson
- Correa Guadalupe, Nelson Alfredo *(código)*
- Limache Santana, Ernesto Gabriel
""")
