import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

# Configuración de la página
st.set_page_config(page_title="Análisis Descriptivo", page_icon="📈", layout="wide")

# Función para cargar datos
@st.cache_data
def cargar_datos():
    ruta_base = Path(__file__).parent.parent
    ruta_datos = ruta_base / 'data' / 'encuesta_recreacion.csv'
    return pd.read_csv(ruta_datos)

# Cargar datos
df = cargar_datos()

# Título de la página
st.title("📈 Análisis Descriptivo")

# Mostrar datos crudos
st.header("1.1 Datos Crudos")
st.dataframe(
    df,
    hide_index=False,  # Muestra los índices
    column_config={
        "all": st.column_config.Column(
            width="medium",
        ),
    },
    use_container_width=True
)

# Agregar información sobre cómo copiar
st.info('💡 Para copiar datos: Selecciona las celdas que deseas copiar, presiona Ctrl+C (o Cmd+C en Mac), y pégalos en Excel o Word.')

# Tabs para diferentes análisis
tab1, tab2, tab3 = st.tabs(["Variables y Tipos", "Gráficos", "Medidas Estadísticas"])

with tab1:
    st.header("2.2 Variables y Tipos de Variables")
    
    # Definir tipos de variables con mapeo especial para la tabla
    variables_tabla = {
        "Edad": ["1", "¿Cuál es tu edad?", "Cuantitativa discreta"],
        "Género": ["2", "¿Cuál es tu género?", "Cualitativa nominal"],
        "Ubicación del Centro": ["3", "¿Dónde se encuentra el parque o centro recreativo que más frecuentas?", "Cualitativa nominal"],
        "Frecuencia de Visitas": ["4", "¿Cuántas veces visitas el centro recreativo por semana?", "Cualitativa ordinal"],
        "Actividades": ["5", "¿Cuántas actividades presenta el centro recreativo que frecuentas?", "Cualitativa ordinal"],
        "Compañía": ["6", "¿Con cuántas personas normalmente visitas el centro recreativo?", "Cualitativa ordinal"],
        "Residencia": ["7", "¿Dónde resides en relación con el centro recreativo que visitas?", "Cualitativa nominal"],
        "Preferencia": ["8", "¿Cómo calificarías tu preferencia por este centro recreativo?", "Cualitativa ordinal"],
        "Importancia del Costo de Entrada": ["9", "¿Qué tan importante es el costo de entrada para ti al elegir un centro de recreación?", "Cualitativa ordinal"],
        "Época del Año de Visita Frecuente": ["10", "¿En qué épocas del año sueles visitar más los centros de recreación?", "Cualitativa nominal"],
        "Satisfacción": ["11", "¿Qué tan satisfecho estás con los centros de recreación que has visitado?", "Cualitativa ordinal"]
    }
    
    # Crear DataFrame para la tabla de variables
    var_df = pd.DataFrame([
        [item[0], item[1], item[2]] for item in variables_tabla.values()
    ], columns=["ITEM", "VARIABLE", "TIPO"])
    
    # Mostrar tabla de variables
    st.dataframe(var_df, use_container_width=True)
    
    # Explicación de tipos de variables
    st.markdown("""
    ### Explicación de Tipos de Variables:
    
    1. **Variables Cualitativas Nominales**: 
        - Categorías sin orden específico
        - Ejemplos: Género, Ubicación, Residencia
    
    2. **Variables Cualitativas Ordinales**:
        - Categorías con un orden natural
        - Ejemplos: Frecuencia de Visitas, Satisfacción
    
    3. **Variables Cuantitativas Discretas**:
        - Valores numéricos contables
        - Ejemplo: Edad
    """)

with tab2:
    st.header("2.4 Gráficos y Tablas Estadísticas")
    
    # Selector de variable
    columnas_nombres = {
        'Edad': 'Edad',
        'Género': 'Género',
        'Ubicación del Centro': 'Ubicación del Centro',
        'Frecuencia de Visitas': 'Frecuencia de Visitas',
        'Actividades': 'Actividades',
        'Compañía': 'Compañía',
        'Residencia': 'Residencia',
        'Preferencia': 'Preferencia',
        'Importancia del Costo de Entrada': 'Importancia del Costo de Entrada',
        'Época del Año de Visita Frecuente': 'Época del Año de Visita Frecuente',
        'Satisfacción': 'Satisfacción'
    }
    
    variable_seleccionada = st.selectbox(
        "Seleccione la variable a analizar",
        list(columnas_nombres.keys())
    )
    
    # Selector de tipo de gráfico
    tipo_grafico = st.radio(
        "Seleccione el tipo de gráfico",
        ["Barras", "Pie (Pizza)"],
        horizontal=True
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráficos
        if variable_seleccionada == 'Edad':
            # Manejo especial para variable numérica Edad
            counts = pd.DataFrame({
                'Categoría': df[columnas_nombres[variable_seleccionada]].astype(str),
                'Cantidad': 1
            }).groupby('Categoría').count().reset_index()
        else:
            # Para variables categóricas
            counts = df[columnas_nombres[variable_seleccionada]].value_counts().reset_index()
            counts.columns = ['Categoría', 'Cantidad']
        
        # Crear una copia de counts para los gráficos (sin el Total)
        counts_for_plot = counts.copy()
        
        # Calcular porcentajes para el gráfico
        total = counts_for_plot['Cantidad'].sum()
        counts_for_plot['Porcentaje'] = (counts_for_plot['Cantidad'] / total * 100).round(2)

        # Crear gráficos con counts_for_plot (sin el Total)
        if tipo_grafico == "Barras":
            fig = px.bar(
                counts_for_plot,
                x='Categoría',
                y='Cantidad',
                title=f"Distribución de {variable_seleccionada}",
                text='Cantidad'
            )
            fig.update_traces(textposition='outside')
        else:  # Pie
            fig = px.pie(
                counts_for_plot,
                values='Cantidad',
                names='Categoría',
                title=f"Distribución de {variable_seleccionada}",
                hole=0.3
            )
            fig.update_traces(textposition='outside', textinfo='percent+label')

        st.plotly_chart(fig, use_container_width=True)

        # Preparar datos para la tabla de frecuencias
        counts['Porcentaje'] = (counts['Cantidad'] / total * 100).round(2)
        
        # Agregar fila de total
        totals = pd.DataFrame({
            'Categoría': ['Total'],
            'Cantidad': [total],
            'Porcentaje': [100.00]
        })
        
        # Convertir todos los números a tipo float para evitar problemas de conversión
        counts['Cantidad'] = counts['Cantidad'].astype(float)
        counts['Porcentaje'] = counts['Porcentaje'].astype(float)
        
        # Concatenar con los totales solo para la tabla
        counts_with_total = pd.concat([counts, totals], ignore_index=True)
        
        # Mostrar tabla de frecuencias
        st.subheader("Tabla de Frecuencias")
        st.dataframe(
            counts_with_total,
            hide_index=True,
            column_config={
                "Cantidad": st.column_config.NumberColumn(format="%d"),
                "Porcentaje": st.column_config.NumberColumn(format="%.2f%%")
            },
            use_container_width=True
        )
        
        # Agregar información sobre cómo copiar
        st.info('💡 Para copiar la tabla: Selecciona las celdas, presiona Ctrl+C (o Cmd+C en Mac), y pégalas en Excel o Word.')

with tab3:
    st.header("2.5 Medidas de Tendencia Central y Dispersión")
    
    # Convertir frecuencia de visitas a numérico
    frecuencia_map = {
        '1 vez': 1,
        '2-3 veces': 2.5,
        '4-5 veces': 4.5,
        'Más de 5 veces': 6
    }
    df_num = df.copy()
    df_num['Frecuencia de Visitas (Numérico)'] = df_num['Frecuencia de Visitas'].map(frecuencia_map)
    
    # Seleccionar variables numéricas/ordinales para análisis
    variables_numericas = ["Preferencia", "Frecuencia de Visitas (Numérico)"]
    
    variable_num = st.selectbox(
        "Seleccione la variable para análisis numérico",
        variables_numericas
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2.5.1 Medidas de Tendencia Central")
        data = df_num[variable_num] if variable_num == "Frecuencia de Visitas (Numérico)" else df[variable_num]
        
        if variable_num == "Frecuencia de Visitas (Numérico)":
            moda_original = df['Frecuencia de Visitas'].mode()[0]
        else:
            moda_original = data.mode()[0]
        
        medidas_centrales = {
            "Media": np.mean(data),
            "Mediana": np.median(data),
            "Moda": moda_original if variable_num == "Frecuencia de Visitas (Numérico)" else data.mode()[0]
        }
        
        for medida, valor in medidas_centrales.items():
            if medida == "Moda":
                st.metric(medida, valor)
            else:
                st.metric(medida, f"{valor:.2f}")
    
    with col2:
        st.subheader("2.5.2 Medidas de Dispersión")
        
        medidas_dispersion = {
            "Varianza": np.var(data),
            "Desviación Estándar": np.std(data),
            "Coeficiente de Variación": (np.std(data) / np.mean(data)) * 100
        }
        
        for medida, valor in medidas_dispersion.items():
            st.metric(medida, f"{valor:.2f}")
    
    # Visualización de la distribución
    st.subheader("Distribución de la Variable")
    if variable_num == "Frecuencia de Visitas (Numérico)":
        fig = px.histogram(
            df_num, 
            x=variable_num,
            title=f"Distribución de Frecuencia de Visitas",
            nbins=10
        )
        # Personalizar etiquetas del eje x
        fig.update_xaxes(
            ticktext=['1 vez', '2-3 veces', '4-5 veces', 'Más de 5 veces'],
            tickvals=[1, 2.5, 4.5, 6]
        )
    else:
        fig = px.histogram(
            df, 
            x=variable_num,
            title=f"Distribución de {variable_num}",
            nbins=20
        )
    st.plotly_chart(fig, use_container_width=True)

# Información adicional en el sidebar
with st.sidebar:
    st.header("📊 Información del Dataset")
    st.write(f"**Total de encuestados:** {len(df)}")
    st.write(f"**Número de variables:** {len(df.columns)}")
    
    st.markdown("---")
    st.markdown("""
    ### 📝 Notas:
    - Los gráficos son interactivos
    - Puede hacer zoom y descargarlos
    - Las tablas muestran frecuencias absolutas y relativas
    """)
