import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

# Configuración de la página
st.set_page_config(page_title="Pruebas de Hipótesis", page_icon="📋", layout="wide")

# Función para cargar datos
@st.cache_data
def cargar_datos():
    ruta_base = Path(__file__).parent.parent
    ruta_datos = ruta_base / 'data' / 'encuesta_recreacion.csv'
    return pd.read_csv(ruta_datos)

# Cargar datos
df = cargar_datos()

# Título de la página
st.title("📋 Pruebas de Hipótesis")

# Convertir satisfacción a numérica para análisis
satisfaccion_map = {
    'Poco satisfecho': 1, 'Poco satisfecha': 1,
    'Satisfecho': 2, 'Satisfecha': 2,
    'Muy satisfecho': 3, 'Muy satisfecha': 3
}
df['Satisfaccion_num'] = df['Satisfacción'].map(satisfaccion_map)

# Selección de prueba
tipo_prueba = st.selectbox(
    "Seleccione el tipo de prueba",
    ["Media", "Proporción", "Chi-cuadrado", "No Paramétrica"]
)

if tipo_prueba == "Media":
    st.header("3.1 Prueba de Hipótesis para la Media")
    
    # Parámetros
    col1, col2 = st.columns(2)
    with col1:
        h0_media = st.number_input("Hipótesis nula (H₀)", value=3.0, step=0.1)
        alpha = st.slider("Nivel de significancia", 0.01, 0.10, 0.05)
    
    # Realizar prueba
    data = df['Preferencia']
    t_stat, p_valor = stats.ttest_1samp(data, h0_media)
    
    # Mostrar resultados
    st.subheader("Resultados")
    col1, col2, col3 = st.columns(3)
    col1.metric("Estadístico t", f"{t_stat:.3f}")
    col2.metric("Valor p", f"{p_valor:.3f}")
    col3.metric("Media muestral", f"{np.mean(data):.3f}")
    
    # Interpretación
    st.subheader("Interpretación")
    if p_valor < alpha:
        st.error(f"Se rechaza H₀ (p-valor = {p_valor:.3f} < {alpha})")
    else:
        st.success(f"No se rechaza H₀ (p-valor = {p_valor:.3f} > {alpha})")

elif tipo_prueba == "Proporción":
    st.header("3.3 Prueba de Hipótesis para la Proporción")
    
    # Parámetros
    col1, col2 = st.columns(2)
    with col1:
        h0_prop = st.slider("Proporción hipotética (H₀)", 0.0, 1.0, 0.5)
        alpha = st.slider("Nivel de significancia", 0.01, 0.10, 0.05)
    
    # Calcular proporción de satisfechos
    satisfechos = df['Satisfaccion_num'] >= 2
    p_hat = np.mean(satisfechos)
    n = len(df)
    
    # Realizar prueba
    z_stat = (p_hat - h0_prop) / np.sqrt(h0_prop * (1-h0_prop) / n)
    p_valor = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    # Mostrar resultados
    st.subheader("Resultados")
    col1, col2, col3 = st.columns(3)
    col1.metric("Estadístico Z", f"{z_stat:.3f}")
    col2.metric("Valor p", f"{p_valor:.3f}")
    col3.metric("Proporción muestral", f"{p_hat:.3f}")
    
    # Interpretación
    st.subheader("Interpretación")
    if p_valor < alpha:
        st.error(f"Se rechaza H₀ (p-valor = {p_valor:.3f} < {alpha})")
    else:
        st.success(f"No se rechaza H₀ (p-valor = {p_valor:.3f} > {alpha})")

elif tipo_prueba == "Chi-cuadrado":
    st.header("3.4 Prueba Chi-cuadrado de Independencia")
    
    # Selección de variables
    col1, col2 = st.columns(2)
    with col1:
        var1 = st.selectbox("Variable 1", ["Género", "Edad", "Ubicación del Centro"])
        var2 = st.selectbox("Variable 2", ["Satisfacción", "Frecuencia de Visitas", "Actividades"])
        alpha = st.slider("Nivel de significancia", 0.01, 0.10, 0.05)
    
    # Crear tabla de contingencia
    contingencia = pd.crosstab(df[var1], df[var2])
    
    # Realizar prueba
    chi2, p_valor, gl, esperados = stats.chi2_contingency(contingencia)
    
    # Mostrar resultados
    st.subheader("Resultados")
    col1, col2, col3 = st.columns(3)
    col1.metric("Estadístico χ²", f"{chi2:.3f}")
    col2.metric("Valor p", f"{p_valor:.3f}")
    col3.metric("Grados de libertad", str(gl))
    
    # Mostrar tabla de contingencia
    st.subheader("Tabla de Contingencia")
    st.dataframe(contingencia)
    
    # Interpretación
    st.subheader("Interpretación")
    if p_valor < alpha:
        st.error(f"Se rechaza H₀ (p-valor = {p_valor:.3f} < {alpha})")
        st.write("Existe evidencia de asociación entre las variables.")
    else:
        st.success(f"No se rechaza H₀ (p-valor = {p_valor:.3f} > {alpha})")
        st.write("No hay evidencia suficiente de asociación entre las variables.")

else:  # No Paramétrica
    st.header("3.5 Pruebas No Paramétricas")
    
    # Selección de prueba
    prueba_np = st.selectbox(
        "Seleccione la prueba",
        ["Mann-Whitney U", "Kruskal-Wallis H"]
    )
    
    if prueba_np == "Mann-Whitney U":
        # Comparar preferencias entre géneros
        grupo1 = df[df['Género'] == 'Masculino']['Preferencia']
        grupo2 = df[df['Género'] == 'Femenino']['Preferencia']
        
        # Realizar prueba
        stat, p_valor = stats.mannwhitneyu(grupo1, grupo2, alternative='two-sided')
        
        # Mostrar resultados
        st.subheader("Resultados Mann-Whitney U")
        col1, col2 = st.columns(2)
        col1.metric("Estadístico U", f"{stat:.3f}")
        col2.metric("Valor p", f"{p_valor:.3f}")
        
        # Interpretación
        st.subheader("Interpretación")
        if p_valor < 0.05:
            st.error(f"Se rechaza H₀ (p-valor = {p_valor:.3f} < 0.05)")
            st.write("Existe diferencia significativa en las preferencias entre géneros.")
        else:
            st.success(f"No se rechaza H₀ (p-valor = {p_valor:.3f} > 0.05)")
            st.write("No hay evidencia de diferencia en las preferencias entre géneros.")
    
    else:  # Kruskal-Wallis
        # Comparar preferencias entre grupos de edad
        stat, p_valor = stats.kruskal(*[group['Preferencia'].values 
                                      for name, group in df.groupby('Edad')])
        
        # Mostrar resultados
        st.subheader("Resultados Kruskal-Wallis H")
        col1, col2 = st.columns(2)
        col1.metric("Estadístico H", f"{stat:.3f}")
        col2.metric("Valor p", f"{p_valor:.3f}")
        
        # Interpretación
        st.subheader("Interpretación")
        if p_valor < 0.05:
            st.error(f"Se rechaza H₀ (p-valor = {p_valor:.3f} < 0.05)")
            st.write("Existe diferencia significativa en las preferencias entre grupos de edad.")
        else:
            st.success(f"No se rechaza H₀ (p-valor = {p_valor:.3f} > 0.05)")
            st.write("No hay evidencia de diferencia en las preferencias entre grupos de edad.")

# Información en el sidebar
with st.sidebar:
    st.header("📊 Información")
    st.write(f"**Tamaño de muestra:** {len(df)}")
    
    st.markdown("---")
    st.markdown("""
    ### 📝 Notas:
    - Todas las pruebas usan nivel de significancia α = 0.05 por defecto
    - Las interpretaciones son automáticas basadas en el valor p
    - Los resultados incluyen estadísticos de prueba y valores p
    """)
