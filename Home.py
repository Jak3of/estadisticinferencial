import streamlit as st

st.set_page_config(
    page_title="Análisis Estadístico",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sistema de Análisis Estadístico")
st.markdown("""
### Bienvenido al Sistema de Análisis de Encuesta de Recreación

Este sistema te permite realizar diferentes tipos de análisis estadísticos sobre los datos de la encuesta.

#### Secciones disponibles:

1. **📈 Análisis Descriptivo**
   - Visualización de variables
   - Gráficos de distribución
   - Tablas de frecuencia

2. **🔍 Análisis Inferencial** (Próximamente)
   - Correlaciones
   - Pruebas estadísticas
   - Análisis avanzados

3. **📋 Reportes** (Próximamente)
   - Resúmenes estadísticos
   - Conclusiones
   - Exportación de resultados

Selecciona una sección del menú lateral para comenzar.
""")

# Información del dataset
st.sidebar.header("ℹ️ Información")
st.sidebar.markdown("""
- Total de encuestados: 30
- Variables analizadas: 11
- Última actualización: 2024
""")
