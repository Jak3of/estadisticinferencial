import streamlit as st
import numpy as np
from scipy import stats
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

def latex_copyable(formula, label=""):
    """Muestra una fórmula LaTeX con un botón para copiar."""
    col1, col2 = st.columns([4, 1])
    with col1:
        st.latex(formula)
    with col2:
        if st.button(f"📋 Copiar", key=f"copy_{label}"):
            try:
                st.code(formula, language="latex")
                st.toast("¡Fórmula mostrada! Puedes copiarla desde el bloque de código", icon="✅")
            except Exception as e:
                st.error(f"Error al mostrar la fórmula: {str(e)}")

# Configuración de la página
st.set_page_config(
    page_title="Pruebas de Hipótesis",
    page_icon="📊",
    layout="wide"
)

# Función para cargar datos
@st.cache_data(ttl=0)
def cargar_datos():
    ruta_base = Path(__file__).parent.parent
    ruta_datos = ruta_base / 'data' / 'encuesta_recreacion_numerica.csv'
    df = pd.read_csv(ruta_datos)
    return df

# Cargar datos
df = cargar_datos()

# Configuración de variables
config_variables = {
    'Edad': {
        'descripcion': 'la edad',
        'unidad': 'años',
        'periodo': ''
    },
    'Frecuencia_Visitas': {
        'descripcion': 'la frecuencia de visitas',
        'unidad': 'veces',
        'periodo': 'por mes'
    },
    'Satisfaccion': {
        'descripcion': 'el nivel de satisfacción',
        'unidad': 'puntos',
        'periodo': ''
    },
    'Preferencia': {
        'descripcion': 'el nivel de preferencia',
        'unidad': 'puntos',
        'periodo': ''
    }
}

# Título principal
st.title("CAPÍTULO 3: Pruebas de Hipótesis")

# Crear pestañas principales
main_tabs = st.tabs([
    "1. Pruebas de Hipótesis Estadística",
    "2. Pruebas No Paramétricas"
])

# 1. Pruebas de Hipótesis Estadística
with main_tabs[0]:
    st.header("1. Pruebas de Hipótesis Estadística")
    
    # Crear subtabs para cada tipo de prueba
    pruebas_tabs = st.tabs([
        "1.1 Media (σ² conocida)",
        "1.2 Media (σ² desconocida)",
        "1.3 Diferencia de Medias (σ² conocida)",
        "1.4 Diferencia de Medias (σ² desconocida iguales)",
        "1.5 Diferencia de Medias (σ² desconocida diferentes)",
        "1.6 Proporción",
        "1.7 Diferencia de Proporciones",
        "1.8 Varianza"
    ])
    
    # 1.1 Media con varianza conocida
    with pruebas_tabs[0]:
        st.write("## 1.1 Prueba de Hipótesis para la Media (σ² conocida)")
        
        st.write("""
        ### Ejemplo: Edad Promedio de Visitantes
        
        **Contexto del Problema:**  
        Estudios previos en centros recreativos similares han determinado que la edad promedio de los 
        visitantes es de 25 años, con una desviación estándar poblacional conocida de 5 años. El 
        administrador de "Aventura Park" cree que la edad promedio de sus visitantes es diferente 
        y desea verificar esta afirmación.
        
        **Planteamiento:**
        - Variable de estudio: Edad de los visitantes
        - Tamaño de muestra: 30 visitantes
        - Desviación estándar poblacional (σ): 5 años
        - Nivel de significancia (α): 0.05
        
        **Hipótesis:**  
        - H₀: μ = 25 (La edad promedio de los visitantes es igual a 25 años)
        - H₁: μ ≠ 25 (La edad promedio de los visitantes es diferente de 25 años)
        
        **Tipo de Prueba:** Bilateral (nos interesa detectar diferencias en ambas direcciones)
        """)
        
        # Cálculos con valores fijos
        variable = 'Edad'
        mu0 = 25  # Valor hipotético fijo
        sigma = 5  # Desviación estándar poblacional conocida
        alpha = 0.05  # Nivel de significancia fijo
        
        # Estadísticos de la muestra
        n = len(df[variable])
        media_muestral = df[variable].mean()
        z_calc = (media_muestral - mu0) / (sigma / np.sqrt(n))
        
        # Valores críticos para prueba bilateral
        z_crit = stats.norm.ppf(1 - alpha/2)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_calc)))
        
        # Mostrar resultados
        st.write("### Resultados")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"""
            **Datos:**
            - Tamaño de muestra (n) = {n}
            - Media muestral (x̄) = {media_muestral:.2f} años
            - Valor a probar (μ₀) = {mu0:.2f} años
            - Desviación estándar poblacional (σ) = {sigma:.2f}
            - Nivel de significancia (α) = {alpha}
            """)
            
        with col2:
            st.write(f"""
            **Estadísticos:**
            - Z calculado = {z_calc:.4f}
            - Z crítico = ±{z_crit:.4f}
            - Valor p = {p_value:.4f}
            """)
        
        # Fórmula del estadístico
        st.write("### Fórmula del Estadístico de Prueba")
        st.write("Como la varianza poblacional es conocida, usamos la distribución normal Z:")
        formula = r"Z = \frac{\bar{x} - \mu_0}{\sigma/\sqrt{n}}"
        latex_copyable(formula, "z_media")
        
        # Resolución paso a paso
        st.write("### Resolución")
        st.write("**Paso 1: Identificar los valores**")
        st.write(f"""
        - Media muestral (x̄) = {media_muestral:.4f}
        - Media hipotética (μ₀) = {mu0:.4f}
        - Desviación estándar poblacional (σ) = {sigma:.4f}
        - Tamaño de muestra (n) = {n}
        """)
        
        st.write("**Paso 2: Sustituir en la fórmula**")
        sustitucion = rf"Z = \frac{{{media_muestral:.4f} - {mu0:.4f}}}{{{sigma:.4f}/\sqrt{{{n}}}}} = \frac{{{media_muestral-mu0:.4f}}}{{{sigma/np.sqrt(n):.4f}}} = {z_calc:.4f}"
        latex_copyable(sustitucion, "z_media_calc")
        
        st.write("**Paso 3: Comparar con el valor crítico**")
        st.write(f"""
        |Z| = |{z_calc:.4f}|
        Valor crítico = ±{z_crit:.4f}
        """)
        
        st.write("**Paso 4: Decisión e Interpretación**")
        if p_value < alpha:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es menor que α ({alpha}), se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, existe evidencia estadística suficiente para concluir que la edad 
            promedio de los visitantes en Aventura Park es diferente de 25 años. Específicamente, la edad promedio 
            observada es de {media_muestral:.2f} años, lo que indica que los visitantes son {"más jóvenes" if media_muestral < mu0 else "mayores"} 
            que lo típicamente observado en centros recreativos similares.
            """)
        else:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es mayor que α ({alpha}), no se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que la edad 
            promedio de los visitantes en Aventura Park es diferente de 25 años. La edad promedio observada de 
            {media_muestral:.2f} años no es estadísticamente diferente de lo típicamente observado en centros recreativos similares.
            """)
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución normal
        x = np.linspace(stats.norm.ppf(0.001), stats.norm.ppf(0.999), 1000)
        y = stats.norm.pdf(x)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva normal
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Normal',
                               line=dict(color='blue')))
        
        # Áreas de rechazo
        # Área de rechazo izquierda
        x_rej_izq = x[x <= -z_crit]
        y_rej_izq = stats.norm.pdf(x_rej_izq)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Área de rechazo derecha
        x_rej_der = x[x >= z_crit]
        y_rej_der = stats.norm.pdf(x_rej_der)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para Z calculado
        fig.add_vline(x=z_calc, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"Z calc = {z_calc:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Hipótesis para la Media de Edad',
            xaxis_title='Estadístico Z',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_hipotesis_media_edad")
        
    # 1.2 Media con varianza desconocida
    with pruebas_tabs[1]:
        st.write("## 1.2 Prueba de Hipótesis para la Media (σ² desconocida)")
        
        st.write("""
        ### Ejemplo: Satisfacción en Centro Recreativo
        
        **Contexto del Problema:**  
        El centro recreativo "Aventura Park" ha estado monitoreando la satisfacción de sus visitantes 
        en una escala del 1 al 5. La administración del parque ha establecido como estándar de calidad 
        un nivel de satisfacción de 4 puntos. El equipo de gestión desea verificar si el nivel actual 
        de satisfacción es diferente del estándar establecido.
        
        **Planteamiento:**
        - Variable de estudio: Nivel de satisfacción de los visitantes
        - Tamaño de muestra: 30 visitantes
        - Nivel de significancia (α): 0.05
        
        **Hipótesis:**  
        - H₀: μ = 4 (El nivel promedio de satisfacción es igual a 4 puntos)
        - H₁: μ ≠ 4 (El nivel promedio de satisfacción es diferente de 4 puntos)
        
        **Tipo de Prueba:** Bilateral (nos interesa detectar diferencias en ambas direcciones)
        """)
        
        # Cálculos con valores fijos
        variable = 'Satisfaccion'
        mu0 = 4  # Valor hipotético fijo
        alpha = 0.05  # Nivel de significancia fijo
        
        # Estadísticos de la muestra
        n = len(df[variable])
        media_muestral = df[variable].mean()
        s = df[variable].std()  # Desviación estándar muestral
        gl = n - 1  # Grados de libertad
        t_calc = (media_muestral - mu0) / (s / np.sqrt(n))
        
        # Valores críticos para prueba bilateral
        t_crit = stats.t.ppf(1 - alpha/2, gl)
        p_value = 2 * (1 - stats.t.cdf(abs(t_calc), gl))
        
        # Mostrar resultados
        st.write("### Resultados")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"""
            **Datos:**
            - Tamaño de muestra (n) = {n}
            - Media muestral (x̄) = {media_muestral:.2f} puntos
            - Valor a probar (μ₀) = {mu0:.2f} puntos
            - Desviación estándar muestral (s) = {s:.2f}
            - Grados de libertad (gl) = {gl}
            - Nivel de significancia (α) = {alpha}
            """)
            
        with col2:
            st.write(f"""
            **Estadísticos:**
            - t calculado = {t_calc:.4f}
            - t crítico = ±{t_crit:.4f}
            - Valor p = {p_value:.4f}
            """)
        
        # Fórmula del estadístico
        st.write("### Fórmula del Estadístico de Prueba")
        st.write("Como la varianza poblacional es desconocida y n ≤ 30, usamos la distribución t-Student:")
        formula = r"t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}"
        latex_copyable(formula, "t_media_12")  # Cambiado de "t_media" a "t_media_12"
        
        # Resolución paso a paso
        st.write("### Resolución")
        st.write("**Paso 1: Identificar los valores**")
        st.write(f"""
        - Media muestral (x̄) = {media_muestral:.4f}
        - Media hipotética (μ₀) = {mu0:.4f}
        - Desviación estándar muestral (s) = {s:.4f}
        - Tamaño de muestra (n) = {n}
        - Grados de libertad (gl) = {gl}
        """)
        
        st.write("**Paso 2: Sustituir en la fórmula**")
        sustitucion = rf"t = \frac{{{media_muestral:.4f} - {mu0:.4f}}}{{{s:.4f}/\sqrt{{{n}}}}} = \frac{{{media_muestral-mu0:.4f}}}{{{s/np.sqrt(n):.4f}}} = {t_calc:.4f}"
        latex_copyable(sustitucion, "t_media_calc_12")  # Cambiado para ser único
        
        st.write("**Paso 3: Comparar con el valor crítico**")
        st.write(f"""
        |t| = |{t_calc:.4f}|
        Valor crítico = ±{t_crit:.4f}
        """)
        
        st.write("**Paso 4: Decisión e Interpretación**")
        if p_value < alpha:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es menor que α ({alpha}), se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, existe evidencia estadística suficiente para concluir que el nivel 
            promedio de satisfacción en Aventura Park es diferente de 4 puntos. Específicamente, el nivel promedio 
            de satisfacción observado es de {media_muestral:.2f} puntos, lo que sugiere que el centro recreativo 
            {"no está alcanzando" if media_muestral < mu0 else "está superando"} el estándar establecido.
            """)
        else:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es mayor que α ({alpha}), no se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que el nivel 
            promedio de satisfacción en Aventura Park es diferente de 4 puntos. El nivel promedio observado de 
            {media_muestral:.2f} puntos no es estadísticamente diferente del estándar establecido.
            """)
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución t
        x = np.linspace(stats.t.ppf(0.001, gl), stats.t.ppf(0.999, gl), 1000)
        y = stats.t.pdf(x, gl)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva t
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución t-Student',
                               line=dict(color='blue')))
        
        # Áreas de rechazo
        # Área de rechazo izquierda
        x_rej_izq = x[x <= -t_crit]
        y_rej_izq = stats.t.pdf(x_rej_izq, gl)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Área de rechazo derecha
        x_rej_der = x[x >= t_crit]
        y_rej_der = stats.t.pdf(x_rej_der, gl)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para t calculado
        fig.add_vline(x=t_calc, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"t calc = {t_calc:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Hipótesis para la Media de Satisfacción',
            xaxis_title='Estadístico t',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_hipotesis_media_satisfaccion")
        
    # 1.3 Diferencia de medias con varianza conocida
    with pruebas_tabs[2]:
        st.write("## 1.3 Prueba de Hipótesis para la Diferencia de Medias (σ² conocida)")
        
        st.write("""
        ### Ejemplo: Frecuencia de Visitas por Grupos de Edad
        
        **Contexto del Problema:**  
        El administrador de Aventura Park quiere comparar la frecuencia de visitas entre dos grupos: 
        jóvenes (≤ 25 años) y adultos (> 25 años). Estudios previos han determinado que la desviación 
        estándar de la frecuencia de visitas es de 1.5 visitas/mes para ambos grupos. Se desea verificar 
        si existe una diferencia significativa en la frecuencia de visitas entre estos grupos.
        
        **Planteamiento:**
        - Variable: Frecuencia de visitas mensuales
        - Grupos:
          * Grupo 1: Visitantes ≤ 25 años
          * Grupo 2: Visitantes > 25 años
        - Desviación estándar conocida (σ₁ = σ₂ = 1.5 visitas/mes)
        - Nivel de significancia (α): 0.05
        
        **Hipótesis:**  
        - H₀: μ₁ - μ₂ = 0 (No hay diferencia en la frecuencia de visitas entre grupos)
        - H₁: μ₁ - μ₂ ≠ 0 (Existe diferencia en la frecuencia de visitas entre grupos)
        
        **Tipo de Prueba:** Bilateral (nos interesa detectar diferencias en ambas direcciones)
        """)
        
        # Cálculos con valores fijos
        variable = 'Frecuencia_Visitas'
        sigma = 1.5  # Desviación estándar poblacional conocida
        alpha = 0.05  # Nivel de significancia fijo
        
        # Crear los grupos
        grupo1 = df[df['Edad'] <= 25][variable]
        grupo2 = df[df['Edad'] > 25][variable]
        
        # Estadísticos de las muestras
        n1 = len(grupo1)
        n2 = len(grupo2)
        media1 = grupo1.mean()
        media2 = grupo2.mean()
        
        # Cálculo del estadístico Z
        z_calc = (media1 - media2) / np.sqrt((sigma**2/n1) + (sigma**2/n2))
        
        # Valores críticos para prueba bilateral
        z_crit = stats.norm.ppf(1 - alpha/2)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_calc)))
        
        # Mostrar resultados
        st.write("### Resultados")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"""
            **Datos Grupo 1 (≤ 25 años):**
            - Tamaño de muestra (n₁) = {n1}
            - Media muestral (x̄₁) = {media1:.2f} visitas/mes
            
            **Datos Grupo 2 (> 25 años):**
            - Tamaño de muestra (n₂) = {n2}
            - Media muestral (x̄₂) = {media2:.2f} visitas/mes
            
            **Parámetros:**
            - Desviación estándar (σ₁ = σ₂) = {sigma:.2f}
            - Nivel de significancia (α) = {alpha}
            """)
            
        with col2:
            st.write(f"""
            **Estadísticos:**
            - Z calculado = {z_calc:.4f}
            - Z crítico = ±{z_crit:.4f}
            - Valor p = {p_value:.4f}
            
            **Diferencia de medias:**
            - x̄₁ - x̄₂ = {media1 - media2:.4f}
            """)
        
        # Fórmula del estadístico
        st.write("### Fórmula del Estadístico de Prueba")
        st.write("Como las varianzas poblacionales son conocidas e iguales, usamos la distribución normal Z:")
        formula = r"Z = \frac{(\bar{x}_1 - \bar{x}_2) - (\mu_1 - \mu_2)_0}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}"
        latex_copyable(formula, "z_diff_medias")
        
        # Resolución paso a paso
        st.write("### Resolución")
        st.write("**Paso 1: Identificar los valores**")
        st.write(f"""
        - Media muestral grupo 1 (x̄₁) = {media1:.4f}
        - Media muestral grupo 2 (x̄₂) = {media2:.4f}
        - Diferencia hipotética (μ₁ - μ₂)₀ = 0
        - Desviación estándar (σ₁ = σ₂) = {sigma:.4f}
        - Tamaños de muestra: n₁ = {n1}, n₂ = {n2}
        """)
        
        st.write("**Paso 2: Sustituir en la fórmula**")
        sustitucion = rf"Z = \frac{{({media1:.4f} - {media2:.4f}) - 0}}{{\sqrt{{\frac{{{sigma:.4f}^2}}{{{n1}}} + \frac{{{sigma:.4f}^2}}{{{n2}}}}}}} = \frac{{{media1-media2:.4f}}}{{{np.sqrt((sigma**2/n1) + (sigma**2/n2)):.4f}}} = {z_calc:.4f}"
        latex_copyable(sustitucion, "z_diff_medias_calc")
        
        st.write("**Paso 3: Comparar con el valor crítico**")
        st.write(f"""
        |Z| = |{z_calc:.4f}|
        Valor crítico = ±{z_crit:.4f}
        """)
        
        st.write("**Paso 4: Decisión e Interpretación**")
        if p_value < alpha:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es menor que α ({alpha}), se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, existe evidencia estadística suficiente para concluir que hay 
            una diferencia significativa en la frecuencia de visitas entre los grupos de edad. El grupo 
            {"joven (≤ 25 años)" if media1 > media2 else "adulto (> 25 años)"} tiene una frecuencia promedio 
            mayor de visitas ({max(media1, media2):.2f} visitas/mes vs {min(media1, media2):.2f} visitas/mes).
            """)
        else:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es mayor que α ({alpha}), no se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que hay 
            una diferencia significativa en la frecuencia de visitas entre los grupos de edad. Aunque el grupo 
            {"joven (≤ 25 años)" if media1 > media2 else "adulto (> 25 años)"} tiene una frecuencia promedio 
            ligeramente mayor ({max(media1, media2):.2f} visitas/mes vs {min(media1, media2):.2f} visitas/mes), 
            esta diferencia no es estadísticamente significativa.
            """)
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución normal
        x = np.linspace(stats.norm.ppf(0.001), stats.norm.ppf(0.999), 1000)
        y = stats.norm.pdf(x)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva normal
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Normal',
                               line=dict(color='blue')))
        
        # Áreas de rechazo
        # Área de rechazo izquierda
        x_rej_izq = x[x <= -z_crit]
        y_rej_izq = stats.norm.pdf(x_rej_izq)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Área de rechazo derecha
        x_rej_der = x[x >= z_crit]
        y_rej_der = stats.norm.pdf(x_rej_der)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para Z calculado
        fig.add_vline(x=z_calc, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"Z calc = {z_calc:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Hipótesis para la Diferencia de Medias en Frecuencia de Visitas',
            xaxis_title='Estadístico Z',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_hipotesis_diferencia_medias")
        
        # Mostrar box plot de comparación
        st.write("### Comparación de Grupos")
        fig_box = go.Figure()
        
        fig_box.add_trace(go.Box(y=grupo1, name='≤ 25 años',
                                boxpoints='all', jitter=0.3, pointpos=-1.8))
        fig_box.add_trace(go.Box(y=grupo2, name='> 25 años',
                                boxpoints='all', jitter=0.3, pointpos=-1.8))
        
        fig_box.update_layout(
            title='Distribución de Frecuencia de Visitas por Grupo de Edad',
            yaxis_title='Frecuencia de Visitas (por mes)',
            showlegend=True
        )
        
        st.plotly_chart(fig_box, use_container_width=True, key="plot_comparacion_grupos")
        
    # 1.4 Diferencia de medias con varianza desconocida iguales
    with pruebas_tabs[3]:
        st.write("## 1.4 Prueba de Hipótesis para la Diferencia de Medias (σ² desconocida iguales)")
        
        st.write("""
        ### Ejemplo: Satisfacción por Género
        
        **Contexto del Problema:**  
        El administrador de Aventura Park ha estado monitoreando la satisfacción de sus visitantes 
        en una escala del 1 al 5. La administración del parque ha establecido como estándar de calidad 
        un nivel de satisfacción de 4 puntos. El equipo de gestión desea verificar si el nivel actual 
        de satisfacción es diferente del estándar establecido.
        
        **Planteamiento:**
        - Variable de estudio: Nivel de satisfacción de los visitantes
        - Tamaño de muestra: 30 visitantes
        - Nivel de significancia (α): 0.05
        
        **Hipótesis:**  
        - H₀: μ = 4 (El nivel promedio de satisfacción es igual a 4 puntos)
        - H₁: μ ≠ 4 (El nivel promedio de satisfacción es diferente de 4 puntos)
        
        **Tipo de Prueba:** Bilateral (nos interesa detectar diferencias en ambas direcciones)
        """)
        
        # Cálculos con valores fijos
        variable = 'Satisfaccion'
        mu0 = 4  # Valor hipotético fijo
        alpha = 0.05  # Nivel de significancia fijo
        
        # Estadísticos de la muestra
        n = len(df[variable])
        media_muestral = df[variable].mean()
        s = df[variable].std()  # Desviación estándar muestral
        gl = n - 1  # Grados de libertad
        t_calc = (media_muestral - mu0) / (s / np.sqrt(n))
        
        # Valores críticos para prueba bilateral
        t_crit = stats.t.ppf(1 - alpha/2, gl)
        p_value = 2 * (1 - stats.t.cdf(abs(t_calc), gl))
        
        # Mostrar resultados
        st.write("### Resultados")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"""
            **Datos:**
            - Tamaño de muestra (n) = {n}
            - Media muestral (x̄) = {media_muestral:.2f} puntos
            - Valor a probar (μ₀) = {mu0:.2f} puntos
            - Desviación estándar muestral (s) = {s:.2f}
            - Grados de libertad (gl) = {gl}
            - Nivel de significancia (α) = {alpha}
            """)
            
        with col2:
            st.write(f"""
            **Estadísticos:**
            - t calculado = {t_calc:.4f}
            - t crítico = ±{t_crit:.4f}
            - Valor p = {p_value:.4f}
            """)
        
        # Fórmula del estadístico
        st.write("### Fórmula del Estadístico de Prueba")
        st.write("Como la varianza poblacional es desconocida y n ≤ 30, usamos la distribución t-Student:")
        formula = r"t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}"
        latex_copyable(formula, "t_media")
        
        # Resolución paso a paso
        st.write("### Resolución")
        st.write("**Paso 1: Identificar los valores**")
        st.write(f"""
        - Media muestral (x̄) = {media_muestral:.4f}
        - Media hipotética (μ₀) = {mu0:.4f}
        - Desviación estándar muestral (s) = {s:.4f}
        - Tamaño de muestra (n) = {n}
        - Grados de libertad (gl) = {gl}
        """)
        
        st.write("**Paso 2: Sustituir en la fórmula**")
        sustitucion = rf"t = \frac{{{media_muestral:.4f} - {mu0:.4f}}}{{{s:.4f}/\sqrt{{{n}}}}} = \frac{{{media_muestral-mu0:.4f}}}{{{s/np.sqrt(n):.4f}}} = {t_calc:.4f}"
        latex_copyable(sustitucion, "t_media_calc")
        
        st.write("**Paso 3: Comparar con el valor crítico**")
        st.write(f"""
        |t| = |{t_calc:.4f}|
        Valor crítico = ±{t_crit:.4f}
        """)
        
        st.write("**Paso 4: Decisión e Interpretación**")
        if p_value < alpha:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es menor que α ({alpha}), se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, existe evidencia estadística suficiente para concluir que el nivel 
            promedio de satisfacción en Aventura Park es diferente de 4 puntos. Específicamente, el nivel promedio 
            de satisfacción observado es de {media_muestral:.2f} puntos, lo que sugiere que el centro recreativo 
            {"no está alcanzando" if media_muestral < mu0 else "está superando"} el estándar establecido.
            """)
        else:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es mayor que α ({alpha}), no se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que el nivel 
            promedio de satisfacción en Aventura Park es diferente de 4 puntos. El nivel promedio observado de 
            {media_muestral:.2f} puntos no es estadísticamente diferente del estándar establecido.
            """)
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución t
        x = np.linspace(stats.t.ppf(0.001, gl), stats.t.ppf(0.999, gl), 1000)
        y = stats.t.pdf(x, gl)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva t
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución t-Student',
                               line=dict(color='blue')))
        
        # Áreas de rechazo
        # Área de rechazo izquierda
        x_rej_izq = x[x <= -t_crit]
        y_rej_izq = stats.t.pdf(x_rej_izq, gl)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Área de rechazo derecha
        x_rej_der = x[x >= t_crit]
        y_rej_der = stats.t.pdf(x_rej_der, gl)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para t calculado
        fig.add_vline(x=t_calc, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"t calc = {t_calc:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Hipótesis para la Media de Satisfacción',
            xaxis_title='Estadístico t',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_hipotesis_media_satisfaccion_2")
        
    # 1.5 Diferencia de medias con varianza desconocida diferentes
    with pruebas_tabs[4]:
        st.write("## 1.5 Prueba de Hipótesis para la Diferencia de Medias (σ² desconocida diferentes)")
        
        st.write("""
        ### Ejemplo: Satisfacción por Género
        
        **Contexto del Problema:**  
        Se realizó una encuesta para determinar si existe diferencia en la satisfacción entre hombres y mujeres 
        en el centro recreativo, suponiendo que las poblaciones son normales pero con varianzas diferentes.
        """)

        # Cálculos con nuestros datos
        grupo1 = df[df['Genero'] == 1]['Satisfaccion']  # Hombres
        grupo2 = df[df['Genero'] == 2]['Satisfaccion']  # Mujeres
        
        n1 = len(grupo1)
        n2 = len(grupo2)
        x1 = grupo1.mean()
        x2 = grupo2.mean()
        s1_2 = grupo1.var()  # varianza grupo 1
        s2_2 = grupo2.var()  # varianza grupo 2
        alpha = 0.05  # Cambiado de 0.1 a 0.05
        
        st.write(f"""
        **Datos:**
        Grupo 1: Hombres
        - n₁ = {n1}
        - x̄₁ = {x1:.2f}
        - s₁² = {s1_2:.2f}

        Grupo 2: Mujeres
        - n₂ = {n2}
        - x̄₂ = {x2:.2f}
        - s₂² = {s2_2:.2f}
        """)

        st.write("""
        **Hipótesis:**
        - H₀: μ₁ = μ₂ (La satisfacción promedio es igual entre hombres y mujeres)
        - H₁: μ₁ ≠ μ₂ (La satisfacción promedio es diferente entre hombres y mujeres)
        """)

        # Paso 3: Estadístico de prueba
        t_calc = (x1 - x2) / np.sqrt(s1_2/n1 + s2_2/n2)
        
        # Paso 6: Grados de libertad (Welch-Satterthwaite)
        v = ((s1_2/n1 + s2_2/n2)**2) / (((s1_2/n1)**2)/(n1-1) + ((s2_2/n2)**2)/(n2-1))
        gl = int(np.floor(v))

        # Paso 4: Valor crítico
        t_crit = stats.t.ppf(1 - alpha/2, gl)

        # P-valor
        p_value = 2 * (1 - stats.t.cdf(abs(t_calc), gl))

        # Mostrar resultados paso a paso
        st.write("### Resolución")
        
        st.write("**Paso 1: Plantear Hipótesis**")
        st.write("H₀: μ₁ = μ₂ vs H₁: μ₁ ≠ μ₂")
        
        st.write("**Paso 2: Nivel de Significancia**")
        st.write(f"α = {alpha} (5%)")
        
        # Calcular las diferencias y los signos para la primera prueba
        diferencias_primera = df['Satisfaccion'] - df['Importancia_Costo']
        signos_primera = np.sign(diferencias_primera)
        n_pos_primera = np.sum(signos_primera > 0)
        n_neg_primera = np.sum(signos_primera < 0)
        n_ceros_primera = np.sum(signos_primera == 0)
        n_efectivo = len(signos_primera) - n_ceros_primera
        
        # Calcular probabilidad binomial
        r = min(n_pos_primera, n_neg_primera) if n_efectivo > 0 else 0
        p_value = 2 * stats.binom.cdf(r, n_efectivo, 0.5) if n_efectivo > 0 else 1.0
        
        st.write(f"""
        **Paso 3: Cálculo del P-valor**
        - r (mínimo entre n⁺ y n⁻) = {r}
        - n efectivo = {n_efectivo}
        - P-valor = {p_value:.4f}
        """)
        
        st.write("### Conclusión")
        if p_value < alpha:
            st.write(f"""
            Con un nivel de significancia del 5%, existe suficiente evidencia estadística para rechazar 
            la hipótesis nula. Por lo tanto, podemos concluir que sí existe una diferencia significativa 
            entre la satisfacción de los visitantes y la importancia que le dan al costo.
            """)
        else:
            st.write(f"""
            Con un nivel de significancia del 5%, no existe suficiente evidencia estadística para rechazar 
            la hipótesis nula. Por lo tanto, no podemos concluir que exista una diferencia significativa 
            entre la satisfacción de los visitantes y la importancia que le dan al costo.
            """)

        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución t
        x = np.linspace(stats.t.ppf(0.001, gl), stats.t.ppf(0.999, gl), 1000)
        y = stats.t.pdf(x, gl)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva t
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución t-Student',
                               line=dict(color='blue')))
        
        # Áreas de rechazo
        # Área de rechazo izquierda
        x_rej_izq = x[x <= -t_crit]
        y_rej_izq = stats.t.pdf(x_rej_izq, gl)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Área de rechazo derecha
        x_rej_der = x[x >= t_crit]
        y_rej_der = stats.t.pdf(x_rej_der, gl)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para t calculado
        fig.add_vline(x=t_calc, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"t calc = {t_calc:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Hipótesis para la Diferencia de Medias (Varianzas Diferentes)',
            xaxis_title='Estadístico t',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_hipotesis_diferencia_medias_varianzas_diferentes")
        
    # 1.6 Proporción
    with pruebas_tabs[5]:
        st.write("## 1.6 Prueba de Hipótesis para una Proporción")
        
        st.write("""
        ### Ejemplo: Proporción de Visitantes Satisfechos
        
        **Contexto del Problema:**  
        El centro recreativo desea evaluar si la proporción de visitantes satisfechos 
        (aquellos que calificaron su satisfacción como 4 o 5) es mayor al 70%.
        
        **Planteamiento:**
        - Variable de estudio: Satisfacción (4 o 5 = Satisfecho)
        - Tamaño de muestra: 30 visitantes
        - Nivel de significancia (α): 0.05
        """)
        
        # Cálculos
        n = len(df)
        satisfechos = len(df[df['Satisfaccion'] >= 4])
        p_muestra = satisfechos / n
        p0 = 0.70  # Proporción hipotética
        alpha = 0.05
        
        # Estadístico de prueba
        z_calc = (p_muestra - p0) / np.sqrt(p0 * (1 - p0) / n)
        
        # Valor crítico
        z_crit = stats.norm.ppf(1 - alpha)  # Prueba unilateral derecha
        
        # P-valor
        p_value = 1 - stats.norm.cdf(z_calc)
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución normal
        x = np.linspace(stats.norm.ppf(0.001), stats.norm.ppf(0.999), 1000)
        y = stats.norm.pdf(x)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva normal
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Normal',
                               line=dict(color='blue')))
        
        # Área de rechazo (cola derecha)
        x_rej = x[x >= z_crit]
        y_rej = stats.norm.pdf(x_rej)
        fig.add_trace(go.Scatter(x=x_rej, y=y_rej, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α = {alpha:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para z calculado
        fig.add_vline(x=z_calc, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"z calc = {z_calc:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Hipótesis para la Proporción de Visitantes Satisfechos',
            xaxis_title='Estadístico Z',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_hipotesis_proporcion")
        
    # 1.7 Diferencia de Proporciones
    with pruebas_tabs[6]:
        st.write("## 1.7 Prueba de Hipótesis para la Diferencia de Proporciones")
        
        st.write("""
        ### Ejemplo: Satisfacción por Género
        
        **Contexto del Problema:**  
        El centro recreativo desea evaluar si existe una diferencia significativa en la proporción 
        de visitantes satisfechos (calificación ≥ 4) entre hombres y mujeres.
        
        **Planteamiento:**
        - Variable de estudio: Satisfacción por género
        - Nivel de significancia (α): 0.05
        """)
        
        # Cálculos
        # Grupo 1: Hombres
        df_hombres = df[df['Genero'] == 1]
        n1 = len(df_hombres)
        satisfechos_h = len(df_hombres[df_hombres['Satisfaccion'] >= 4])
        p1 = satisfechos_h / n1
        
        # Grupo 2: Mujeres
        df_mujeres = df[df['Genero'] == 2]
        n2 = len(df_mujeres)
        satisfechos_m = len(df_mujeres[df_mujeres['Satisfaccion'] >= 4])
        p2 = satisfechos_m / n2
        
        # Proporción combinada
        p_comb = (satisfechos_h + satisfechos_m) / (n1 + n2)
        
        # Estadístico de prueba
        z_calc = (p1 - p2) / np.sqrt(p_comb * (1 - p_comb) * (1/n1 + 1/n2))
        
        # Valor crítico (bilateral)
        alpha = 0.05
        z_crit = stats.norm.ppf(1 - alpha/2)
        
        # P-valor
        p_value = 2 * (1 - stats.norm.cdf(abs(z_calc)))
        
        st.write("### Resultados")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"""
            **Grupo 1 (Hombres):**
            - Tamaño de muestra (n₁) = {n1}
            - Satisfechos = {satisfechos_h}
            - Proporción (p₁) = {p1:.4f}
            
            **Grupo 2 (Mujeres):**
            - Tamaño de muestra (n₂) = {n2}
            - Satisfechos = {satisfechos_m}
            - Proporción (p₂) = {p2:.4f}
            """)
            
        with col2:
            st.write(f"""
            **Estadísticos:**
            - Z calculado = {z_calc:.4f}
            - Z crítico = ±{z_crit:.4f}
            - Valor p = {p_value:.4f}
            - Proporción combinada = {p_comb:.4f}
            """)
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución normal
        x = np.linspace(stats.norm.ppf(0.001), stats.norm.ppf(0.999), 1000)
        y = stats.norm.pdf(x)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva normal
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Normal',
                               line=dict(color='blue')))
        
        # Áreas de rechazo
        # Área de rechazo izquierda
        x_rej_izq = x[x <= -z_crit]
        y_rej_izq = stats.norm.pdf(x_rej_izq)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Área de rechazo derecha
        x_rej_der = x[x >= z_crit]
        y_rej_der = stats.norm.pdf(x_rej_der)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para z calculado
        fig.add_vline(x=z_calc, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"z calc = {z_calc:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Hipótesis para la Diferencia de Proporciones',
            xaxis_title='Estadístico Z',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_hipotesis_diferencia_proporciones")
        
        # Interpretación
        st.write("### Interpretación")
        if p_value < alpha:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es menor que α ({alpha}), se rechaza H₀.
            
            **Conclusión:**  
            Con un nivel de confianza del 95%, existe evidencia estadística suficiente para concluir que 
            hay una diferencia significativa en la proporción de visitantes satisfechos entre hombres y mujeres. 
            La diferencia observada de {abs(p1 - p2):.1%} puntos porcentuales es estadísticamente significativa.
            """)
        else:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es mayor que α ({alpha}), no se rechaza H₀.
            
            **Conclusión:**  
            Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que hay 
            una diferencia significativa en la proporción de visitantes satisfechos entre hombres y mujeres. 
            La diferencia observada de {abs(p1 - p2):.1%} puntos porcentuales no es estadísticamente significativa.
            """)

    # 1.8 Varianza
    with pruebas_tabs[7]:
        st.write("## 1.8 Prueba de Hipótesis para la Varianza")
        
        st.write("""
        ### Ejemplo: Varianza de la Satisfacción
        
        **Contexto del Problema:**  
        El centro recreativo desea evaluar si la varianza de la satisfacción de sus visitantes 
        es diferente de 1 punto cuadrado.
        
        **Planteamiento:**
        - Variable de estudio: Satisfacción
        - Tamaño de muestra: 30 visitantes
        - Nivel de significancia (α): 0.05
        """)
        
        # Cálculos
        n = len(df)
        s2 = df['Satisfaccion'].var()
        sigma2_0 = 1  # Varianza hipotética
        alpha = 0.05
        
        # Estadístico de prueba
        chi2_calc = (n - 1) * s2 / sigma2_0
        
        # Valor crítico
        chi2_crit = stats.chi2.ppf(1 - alpha, n - 1)
        
        # P-valor
        p_value = 1 - stats.chi2.cdf(chi2_calc, n - 1)
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución chi-cuadrado
        x = np.linspace(stats.chi2.ppf(0.001, n - 1), stats.chi2.ppf(0.999, n - 1), 1000)
        y = stats.chi2.pdf(x, n - 1)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva chi-cuadrado
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Chi-Cuadrado',
                               line=dict(color='blue')))
        
        # Área de rechazo (cola derecha)
        x_rej = x[x >= chi2_crit]
        y_rej = stats.chi2.pdf(x_rej, n - 1)
        fig.add_trace(go.Scatter(x=x_rej, y=y_rej, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α = {alpha:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para chi2 calculado
        fig.add_vline(x=chi2_calc, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"chi2 calc = {chi2_calc:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Hipótesis para la Varianza de la Satisfacción',
            xaxis_title='Estadístico Chi-Cuadrado',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_hipotesis_varianza")
        
# Prueba de Signos: Importancia del Costo vs Preferencia
st.markdown("### Prueba de Signos: Importancia del Costo vs Preferencia")

st.markdown("""
Esta prueba no paramétrica nos permitirá comparar si existe una diferencia significativa entre 
la importancia que los visitantes le dan al costo y su nivel de preferencia por el lugar.
""")

# Calcular las diferencias y los signos
diferencias = df['Importancia_Costo'] - df['Preferencia']
signos = np.sign(diferencias)

# Contar los signos positivos, negativos y ceros
n_pos = np.sum(signos > 0)
n_neg = np.sum(signos < 0)
n_ceros = np.sum(signos == 0)

# 2. Pruebas No Paramétricas
with main_tabs[1]:
    st.header("2. Pruebas No Paramétricas")
    
    # Crear subtabs para cada tipo de prueba no paramétrica
    no_param_tabs = st.tabs([
        "2.1 Prueba de Signos",
        "2.2 Prueba de Rachas"
    ])
    
    # 2.1 Prueba de signos
    with no_param_tabs[0]:
        st.write("## 2.1 Prueba de Signos")
        
        st.write("""
        ### Ejemplo: Importancia del Costo vs Preferencia
        
        Se desea analizar si existe una diferencia significativa entre la importancia que los visitantes 
        le dan al costo y su nivel de preferencia por el lugar. ¿La importancia del costo tiende a ser 
        diferente a la preferencia? Utilizaremos un nivel de significancia del 5%.
        """)
        
        # Preparar los datos y calcular diferencias
        datos = pd.DataFrame({
            'ID': df.index + 1,
            'Importancia_Costo': df['Importancia_Costo'],
            'Preferencia': df['Preferencia'],
            'Diferencia': df['Importancia_Costo'] - df['Preferencia']
        })
        
        # Calcular signos
        datos['Signo'] = datos['Diferencia'].apply(lambda x: '+' if x > 0 else ('-' if x < 0 else '0'))
        
        # Mostrar tabla de datos
        st.write("**Datos y Signos:**")
        st.dataframe(datos)
        
        # Cálculos para la prueba
        n_total = len(datos)
        n_pos = sum(datos['Signo'] == '+')
        n_neg = sum(datos['Signo'] == '-')
        n_ceros = sum(datos['Signo'] == '0')
        n_efectivo = n_total - n_ceros  # excluyendo empates
        
        st.write(f"""
        **Resumen de Signos:**
        - Total de observaciones: {n_total}
        - Diferencias positivas (IC > P): {n_pos}
        - Diferencias negativas (IC < P): {n_neg}
        - Empates (IC = P): {n_ceros}
        - n efectivo (sin empates): {n_efectivo}
        """)
        
        st.write("### Prueba de Hipótesis")
        
        st.write("""
        **Paso 1: Plantear Hipótesis**
        - H₀: Me = 0 (No hay diferencia entre Importancia del Costo y Preferencia)
        - H₁: Me ≠ 0 (Sí hay diferencia entre Importancia del Costo y Preferencia)
        """)
        
        st.write("**Paso 2: Nivel de Significancia**")
        alpha = 0.05
        st.write(f"α = {alpha}")
        
        # Calcular probabilidad binomial
        r = min(n_pos, n_neg) if n_efectivo > 0 else 0
        p_value = 2 * stats.binom.cdf(r, n_efectivo, 0.5) if n_efectivo > 0 else 1.0
        
        st.write(f"""
        **Paso 3: Cálculo del P-valor**
        - r (mínimo entre n⁺ y n⁻) = {r}
        - n efectivo = {n_efectivo}
        - P-valor = {p_value:.4f}
        """)
        
        st.write("### Conclusión")
        if p_value < alpha:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es menor que α ({alpha}), se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, existe evidencia estadística suficiente para concluir que 
            sí existe una diferencia significativa entre la importancia que los visitantes le dan al costo y su nivel de preferencia por el lugar.
            """)
        else:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es mayor que α ({alpha}), no se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que exista 
            una diferencia significativa entre la importancia que los visitantes le dan al costo y su nivel de preferencia por el lugar.
            """)

        # Visualización
        st.write("### Visualización")
        
        # Aproximación normal para la distribución binomial
        mu = n_efectivo * 0.5  # media bajo H0
        sigma = np.sqrt(n_efectivo * 0.5 * 0.5)  # desviación estándar bajo H0
        
        # Crear datos para la distribución normal
        x = np.linspace(-4, 4, 1000)
        y = stats.norm.pdf(x)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva normal
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Normal',
                               line=dict(color='blue')))
        
        # Áreas de rechazo
        x_rej_izq = x[x <= -z_crit]
        y_rej_izq = stats.norm.pdf(x_rej_izq)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        x_rej_der = x[x >= z_crit]
        y_rej_der = stats.norm.pdf(x_rej_der)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Calcular el Z-score para el valor observado
        z_obs = (r - mu) / sigma
        
        # Agregar línea vertical para el valor observado
        fig.add_vline(x=z_obs, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"z obs = {z_obs:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Signos (Aproximación Normal)',
            xaxis_title='Estadístico Z',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_prueba_signos")
        
    # 2.2 Prueba de rachas
    with no_param_tabs[1]:
        st.write("## 2.2 Prueba de Rachas")
        
        st.write("""
        ### Ejemplo: Aleatoriedad en la Satisfacción
        
        Se desea evaluar si los niveles de satisfacción de los visitantes siguen un patrón aleatorio 
        o si existe alguna tendencia. Utilizaremos la mediana como punto de referencia para determinar 
        las rachas. Nivel de significancia: 5%.
        """)
        
        # Preparar los datos
        satisfaccion = df['Satisfaccion'].values
        mediana = np.median(satisfaccion)
        
        # Crear secuencia de signos
        signos = ['+' if x >= mediana else '-' for x in satisfaccion]
        
        # Crear DataFrame para visualización
        datos_rachas = pd.DataFrame({
            'ID': df.index + 1,
            'Satisfaccion': satisfaccion,
            'Signo': signos
        })
        
        # Mostrar tabla de datos
        st.write("**Datos y Signos:**")
        st.write(f"Mediana de Satisfacción = {mediana}")
        st.write(datos_rachas)
        
        # Contar rachas
        n_rachas = 1
        for i in range(1, len(signos)):
            if signos[i] != signos[i-1]:
                n_rachas += 1
        
        # Contar signos
        n1 = sum(1 for s in signos if s == '+')  # número de valores >= mediana
        n2 = sum(1 for s in signos if s == '-')  # número de valores < mediana
        n = n1 + n2
        
        # Cálculos estadísticos
        # Media y varianza del número de rachas bajo H0
        media_r = 1 + (2 * n1 * n2) / n
        var_r = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n * n * (n - 1))
        
        # Estadístico Z
        z_calc = (n_rachas - media_r) / np.sqrt(var_r)
        
        # Valores críticos y p-valor (prueba bilateral)
        alpha = 0.05
        z_crit = stats.norm.ppf(1 - alpha/2)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_calc)))
        
        st.write("""
        ### Prueba de Hipótesis
        
        **Paso 1: Plantear Hipótesis**
        - H₀: La secuencia es aleatoria
        - H₁: La secuencia no es aleatoria
        """)
        
        st.write(f"""
        **Paso 2: Estadísticos**
        - Número de rachas (R) = {n_rachas}
        - n₁ (≥ mediana) = {n1}
        - n₂ (< mediana) = {n2}
        - Media de R = {media_r:.4f}
        - Varianza de R = {var_r:.4f}
        - Z calculado = {z_calc:.4f}
        - Z crítico = ±{z_crit:.4f}
        - P-valor = {p_value:.4f}
        """)
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución normal
        x = np.linspace(-4, 4, 1000)
        y = stats.norm.pdf(x)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva normal
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Normal',
                               line=dict(color='blue')))
        
        # Áreas de rechazo
        x_rej_izq = x[x <= -z_crit]
        y_rej_izq = stats.norm.pdf(x_rej_izq)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        x_rej_der = x[x >= z_crit]
        y_rej_der = stats.norm.pdf(x_rej_der)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para z calculado
        fig.add_vline(x=z_calc, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"z calc = {z_calc:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Rachas',
            xaxis_title='Estadístico Z',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_prueba_rachas")
        
        # Interpretación
        st.write("### Conclusión")
        if p_value < alpha:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es menor que α ({alpha}), se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, existe evidencia estadística suficiente para concluir que 
            la secuencia de niveles de satisfacción no es aleatoria, lo que sugiere la presencia de algún 
            patrón o tendencia en las calificaciones de los visitantes.
            """)
        else:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es mayor que α ({alpha}), no se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que 
            la secuencia de niveles de satisfacción no sea aleatoria. Los datos sugieren que las calificaciones 
            de satisfacción no siguen ningún patrón específico.
            """)
