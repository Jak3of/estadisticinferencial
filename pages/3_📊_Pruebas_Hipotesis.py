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
        "1.8 Prueba Chi-cuadrado para la Varianza de una Población"
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
            Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que hay una 
            diferencia significativa en la frecuencia de visitas entre los grupos de edad. Aunque el grupo 
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
        
        st.plotly_chart(fig_box, use_container_width=True, key="box_plot_comparacion_grupos")
        
    # 1.4 Diferencia de medias con varianza desconocida iguales
    with pruebas_tabs[3]:
        st.write("## 1.4 Prueba de Hipótesis para la Diferencia de Medias (σ² desconocidas iguales)")
        
        st.write("""
        ### Ejemplo: Satisfacción por Género
        
        **Contexto del Problema:**  
        El administrador de Aventura Park desea investigar si existe una diferencia significativa en los niveles 
        de satisfacción entre visitantes masculinos y femeninos.
        
        **Planteamiento:**
        - Variable de estudio: Nivel de satisfacción de los visitantes por género
        - Hipótesis nula (H₀): No hay diferencia en la satisfacción media entre géneros
        - Nivel de significancia (α): 0.05
        
        **Hipótesis:**  
        - H₀: μ₁ - μ₂ = 0 (No hay diferencia en la satisfacción media entre géneros)
        - H₁: μ₁ - μ₂ ≠ 0 (Existe diferencia en la satisfacción media entre géneros)
        
        **Tipo de Prueba:** Bilateral
        """)
        
        # Separar datos por género
        grupo1 = df[df['Genero'] == 1]['Satisfaccion']
        grupo2 = df[df['Genero'] == 2]['Satisfaccion']
        
        # Verificar que hay suficientes datos en cada grupo
        if len(grupo1) == 0 or len(grupo2) == 0:
            st.error("Error: No hay suficientes datos en uno o ambos grupos.")
        else:
            # Calcular estadísticos
            n1 = len(grupo1)
            n2 = len(grupo2)
            media1 = grupo1.mean()
            media2 = grupo2.mean()
            var1 = grupo1.var(ddof=1)
            var2 = grupo2.var(ddof=1)
            
            # Verificar que las varianzas no son cero
            if var1 == 0 and var2 == 0:
                st.warning("Las varianzas de ambos grupos son cero. Esto significa que todos los valores son idénticos en cada grupo.")
            else:
                # Varianza combinada
                sp2 = ((n1-1)*var1 + (n2-1)*var2)/(n1 + n2 - 2)
                
                # Verificar que la varianza combinada no es cero
                if sp2 <= 0:
                    st.error("Error: La varianza combinada es cero o negativa. No se puede realizar la prueba.")
                else:
                    sp = np.sqrt(sp2)
                    
                    # Estadístico t
                    denominador = sp*np.sqrt(1/n1 + 1/n2)
                    if denominador == 0:
                        st.error("Error: No se puede calcular el estadístico t debido a una división por cero.")
                    else:
                        t_calc = (media1 - media2)/denominador
                        gl = n1 + n2 - 2
                        
                        # Valores críticos
                        alpha = 0.05
                        t_crit = stats.t.ppf(1 - alpha/2, gl)
                        p_value = 2 * (1 - stats.t.cdf(abs(t_calc), gl))
                        
                        # Mostrar resultados
                        st.write("### Resultados")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"""
                            **Datos Grupo 1 (Masculino):**
                            - Tamaño de muestra (n₁) = {n1}
                            - Media muestral (x̄₁) = {media1:.2f}
                            - Varianza muestral (s₁²) = {var1:.2f}
                            
                            **Datos Grupo 2 (Femenino):**
                            - Tamaño de muestra (n₂) = {n2}
                            - Media muestral (x̄₂) = {media2:.2f}
                            - Varianza muestral (s₂²) = {var2:.2f}
                            """)
                            
                        with col2:
                            st.write(f"""
                            **Estadísticos:**
                            - Varianza combinada (sp²) = {sp2:.4f}
                            - Grados de libertad (gl) = {gl}
                            - t calculado = {t_calc:.4f}
                            - t crítico = ±{t_crit:.4f}
                            - Valor p = {p_value:.4f}
                            """)
                        
                        # Fórmulas en LaTeX
                        st.write("### Fórmulas Principales")
                        
                        st.write("**1. Varianza Combinada:**")
                        formula_sp = r"s_p^2 = \frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}"
                        latex_copyable(formula_sp, "sp2")
                        
                        st.write("**2. Estadístico t:**")
                        formula_t = r"t = \frac{\bar{x}_1 - \bar{x}_2}{s_p\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}"
                        latex_copyable(formula_t, "t_stat")
                        
                        st.write("**3. Grados de libertad:**")
                        formula_gl = r"gl = n_1 + n_2 - 2"
                        latex_copyable(formula_gl, "gl")
                        
                        # Resolución paso a paso
                        st.write("### Resolución")
                        
                        st.write("**Paso 1: Calcular la varianza combinada**")
                        formula_sp_calc = rf"s_p^2 = \frac{{({n1}-1){var1:.4f} + ({n2}-1){var2:.4f}}}{{{n1} + {n2} - 2}} = {sp2:.4f}"
                        latex_copyable(formula_sp_calc, "sp2_calc")
                        
                        st.write("**Paso 2: Calcular el estadístico t**")
                        formula_t_calc = rf"t = \frac{{{media1:.4f} - {media2:.4f}}}{{{sp:.4f}\sqrt{{\frac{{1}}{{{n1}}} + \frac{{1}}{{{n2}}}}}}} = {t_calc:.4f}"
                        latex_copyable(formula_t_calc, "t_calc")
                        
                        st.write("**Paso 3: Decisión e Interpretación**")
                        if p_value < alpha:
                            st.write(f"""
                            Como el p-valor ({p_value:.4f}) es menor que α ({alpha}), se rechaza H₀.
                            
                            **Interpretación:**  
                            Con un nivel de confianza del 95%, existe evidencia estadística suficiente para concluir que hay una 
                            diferencia significativa en los niveles de satisfacción entre visitantes masculinos y femeninos. 
                            La diferencia observada es de {media1 - media2:.2f} puntos.
                            """)
                        else:
                            st.write(f"""
                            Como el p-valor ({p_value:.4f}) es mayor que α ({alpha}), no se rechaza H₀.
                            
                            **Interpretación:**  
                            Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que hay una 
                            diferencia significativa en los niveles de satisfacción entre visitantes masculinos y femeninos.
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
                            title='Prueba de Hipótesis para Diferencia de Medias',
                            xaxis_title='Estadístico t',
                            yaxis_title='Densidad',
                            showlegend=True
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Añadir boxplot para visualizar distribución por género
                        fig_box = go.Figure()
                        
                        fig_box.add_trace(go.Box(y=grupo1, name='Masculino',
                                                boxpoints='all', jitter=0.3, pointpos=-1.8))
                        fig_box.add_trace(go.Box(y=grupo2, name='Femenino',
                                                boxpoints='all', jitter=0.3, pointpos=-1.8))
                        
                        fig_box.update_layout(
                            title='Distribución de Satisfacción por Género',
                            yaxis_title='Nivel de Satisfacción',
                            showlegend=True
                        )
                        
                        st.plotly_chart(fig_box, use_container_width=True, key="box_plot_genero")
                        
    # 1.5 Diferencia de medias con varianza desconocida diferentes
    with pruebas_tabs[4]:
        st.write("## 1.5 Prueba de Hipótesis para la Diferencia de Medias (σ² desconocidas diferentes)")
        
        st.write("""
        ### Ejemplo: Satisfacción por Género
        
        **Contexto del Problema:**  
        El administrador de Aventura Park desea investigar si los visitantes masculinos tienen un nivel
        de satisfacción significativamente mayor que las visitantes femeninas, sin asumir que las varianzas son iguales.
        
        **Planteamiento:**
        - Variable de estudio: Nivel de satisfacción de los visitantes por género
        - Hipótesis nula (H₀): Los hombres no tienen mayor satisfacción que las mujeres
        - Nivel de significancia (α): 0.05
        
        **Hipótesis:**  
        - H₀: μ₁ - μ₂ ≤ 0 (Los hombres no tienen mayor satisfacción que las mujeres)
        - H₁: μ₁ - μ₂ > 0 (Los hombres tienen mayor satisfacción que las mujeres)
        
        **Tipo de Prueba:** Unilateral derecha
        """)
        
        # Separar datos por género
        grupo1 = df[df['Genero'] == 1]['Satisfaccion']  # Masculino (1)
        grupo2 = df[df['Genero'] == 2]['Satisfaccion']  # Femenino (2)
        
        # Verificar que hay suficientes datos en cada grupo
        if len(grupo1) == 0 or len(grupo2) == 0:
            st.error("Error: No hay suficientes datos en uno o ambos grupos.")
        else:
            # Calcular estadísticos
            n1 = len(grupo1)
            n2 = len(grupo2)
            media1 = grupo1.mean()
            media2 = grupo2.mean()
            var1 = grupo1.var(ddof=1)
            var2 = grupo2.var(ddof=1)
            
            # Verificar que las varianzas no son cero
            if var1 == 0 and var2 == 0:
                st.warning("Las varianzas de ambos grupos son cero. Esto significa que todos los valores son idénticos en cada grupo.")
            else:
                # Calcular el estadístico t'
                denominador = np.sqrt(var1/n1 + var2/n2)
                if denominador == 0:
                    st.error("Error: No se puede calcular el estadístico t debido a una división por cero.")
                else:
                    t_calc = (media1 - media2)/denominador
                    
                    # Grados de libertad de Welch-Satterthwaite
                    num = (var1/n1 + var2/n2)**2
                    den = (var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1)
                    gl = num/den
                    
                    # Valores críticos (cambio a unilateral)
                    alpha = 0.05
                    t_crit = stats.t.ppf(1 - alpha, gl)  # Ya no dividimos alpha entre 2
                    p_value = 1 - stats.t.cdf(t_calc, gl)  # Solo cola derecha
                    
                    # Mostrar resultados
                    st.write("### Resultados")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"""
                        **Grupo 1 (Masculino):**
                        - Tamaño de muestra (n₁) = {n1}
                        - Media muestral (x̄₁) = {media1:.2f}
                        - Varianza muestral (s₁²) = {var1:.2f}
                        
                        **Grupo 2 (Femenino):**
                        - Tamaño de muestra (n₂) = {n2}
                        - Media muestral (x̄₂) = {media2:.2f}
                        - Varianza muestral (s₂²) = {var2:.2f}
                        """)
                        
                    with col2:
                        st.write(f"""
                        **Estadísticos:**
                        - Grados de libertad (ν) = {gl:.2f}
                        - t' calculado = {t_calc:.4f}
                        - t' crítico = {t_crit:.4f}
                        - Valor p = {p_value:.4f}
                        """)
                    
                    # Fórmulas en LaTeX
                    st.write("### Fórmulas")
                    
                    st.write("**1. Estadístico de Prueba T':**")
                    formula_t = r"T_{cal} = \frac{\bar{X}_1 - \bar{X}_2 - (\mu_1 - \mu_2)_{hip}}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}"
                    latex_copyable(formula_t, "t_welch")
                    
                    st.write("**2. Grados de libertad (Welch-Satterthwaite):**")
                    formula_gl = r"\nu = \frac{(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2})^2}{\frac{(s_1^2/n_1)^2}{n_1-1} + \frac{(s_2^2/n_2)^2}{n_2-1}}"
                    latex_copyable(formula_gl, "gl_welch")
                    
                    st.write("**3. Región de Rechazo:**")
                    formula_rr = r"T_{cal} > t_{\alpha,\nu}"
                    latex_copyable(formula_rr, "rr_welch")
                    
                    st.write("**4. Valor p:**")
                    formula_p = r"p = 1 - F_{t,\nu}(T_{cal})"
                    latex_copyable(formula_p, "p_welch")
                    
                    st.write("**Paso 1: Calcular el estadístico T**")
                    formula_t_calc = rf"T_{{cal}} = \frac{{{media1:.4f} - {media2:.4f} - 0}}{{\sqrt{{\frac{{{var1:.4f}}}{{{n1}}} + \frac{{{var2:.4f}}}{{{n2}}}}}}} = {t_calc:.4f}"
                    latex_copyable(formula_t_calc, "t_welch_calc")
                    
                    st.write("**Paso 2: Calcular los grados de libertad**")
                    formula_gl_calc = rf"\nu = \frac{{(\frac{{{var1:.4f}}}{{{n1}}} + \frac{{{var2:.4f}}}{{{n2}}})^2}}{{\frac{{({var1:.4f}/{n1})^2}}{{{n1}-1}} + \frac{{({var2:.4f}/{n2})^2}}{{{n2}-1}}}} = {gl:.2f}"
                    latex_copyable(formula_gl_calc, "gl_welch_calc")
                    
                    st.write("**Paso 3: Decisión e Interpretación**")
                    if p_value < alpha:
                        st.write(f"""
                        Como el p-valor ({p_value:.4f}) es menor que α ({alpha}), se rechaza H₀.
                        
                        **Interpretación:**  
                        Hay evidencia estadística suficiente para afirmar que los visitantes masculinos tienen
                        un nivel de satisfacción significativamente mayor que las visitantes femeninas
                        (con un nivel de significancia de {alpha}).
                        """)
                    else:
                        st.write(f"""
                        Como el p-valor ({p_value:.4f}) es mayor que α ({alpha}), no se rechaza H₀.
                        
                        **Interpretación:**  
                        No hay evidencia estadística suficiente para concluir que los visitantes masculinos tienen
                        un nivel de satisfacción significativamente mayor que las visitantes femeninas
                        (con un nivel de significancia de {alpha}).
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
                    # Área de rechazo derecha
                    x_rechazo = x[x >= t_crit]
                    y_rechazo = y[x >= t_crit]
                    
                    fig.add_trace(go.Scatter(x=x_rechazo, y=y_rechazo, 
                                           fill='tozeroy', 
                                           fillcolor='rgba(255,0,0,0.3)',
                                           line=dict(color='red'),
                                           name=f'Región de rechazo (α={alpha})'
                                           ))
                    
                    # Agregar línea vertical para t calculado
                    fig.add_vline(x=t_calc, 
                                 line_dash="dash", 
                                 line_color="green",
                                 annotation_text=f"t' calc = {t_calc:.4f}",
                                 annotation_position="top")
                    
                    # Actualizar layout
                    fig.update_layout(
                        title='Prueba de Hipótesis para Diferencia de Medias (Welch)',
                        xaxis_title='Estadístico t\'',
                        yaxis_title='Densidad',
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Añadir boxplot para visualizar distribución por género
                    fig_box = go.Figure()
                    
                    fig_box.add_trace(go.Box(y=grupo1, name='Masculino',
                                            boxpoints='all', jitter=0.3, pointpos=-1.8))
                    fig_box.add_trace(go.Box(y=grupo2, name='Femenino',
                                            boxpoints='all', jitter=0.3, pointpos=-1.8))
                    
                    fig_box.update_layout(
                        title='Distribución de Satisfacción por Género',
                        yaxis_title='Nivel de Satisfacción',
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig_box, use_container_width=True, key="box_plot_genero_2")
                    
    # 1.6 Proporción
    with pruebas_tabs[5]:
        st.write("## 1.6 Prueba de Hipótesis para una Proporción")
        
        st.write("""
        ### Ejemplo: Proporción de Visitantes Satisfechos
        
        Queremos probar si la proporción de visitantes satisfechos (calificación ≥ 4) es igual a 75%.
        
        **Hipótesis:**
        
        H₀: π = 0.75  
        H₁: π ≠ 0.75
        """)
        
        # Mostrar hipótesis en LaTeX
        latex_copyable(r"H_0: \pi = 0.75", "h0_prop")
        latex_copyable(r"H_1: \pi \neq 0.75", "h1_prop")
        
        st.write("**Nivel de significancia:** α = 0.05")
        
        # Calcular proporción muestral
        satisfechos = df[df['Satisfaccion'] >= 4].shape[0]
        total = df.shape[0]
        
        # Mostrar datos
        st.write("""### Datos Muestrales""")
        st.write(f"""
        - Total de visitantes (n): {total}
        - Visitantes satisfechos (x): {satisfechos}
        - Proporción muestral (p̂): {satisfechos/total:.4f}
        - Proporción hipotética (π₀): 0.75
        """)
        
        if total == 0:
            st.error("Error: No hay datos suficientes.")
        else:
            # Calcular estadísticos
            p_hat = satisfechos/total
            pi_0 = 0.75
            
            # Estadístico Z
            denominador = np.sqrt(pi_0*(1-pi_0)/total)
            if denominador == 0:
                st.error("Error: No se puede calcular el estadístico Z debido a una división por cero.")
            else:
                z_calc = (p_hat - pi_0)/denominador
                
                # Valores críticos
                alpha = 0.05
                z_crit = stats.norm.ppf(1 - alpha/2)
                p_value = 2 * (1 - stats.norm.cdf(abs(z_calc)))
                
                # Mostrar resultados
                st.write("### Resultados")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"""
                    **Datos:**
                    - Tamaño de muestra (n) = {total}
                    - Visitantes satisfechos (x) = {satisfechos}
                    - Proporción muestral (p̂) = {p_hat:.4f}
                    - Proporción hipotética (π₀) = {pi_0}
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
                st.write("El estadístico de prueba es:")
                formula = r"Z_c = \frac{\hat{p} - \pi_0}{\sqrt{\frac{\pi_0(1-\pi_0)}{n}}}"
                latex_copyable(formula, "z_prueba")
                
                st.write("Sustituyendo los valores:")
                latex_copyable(rf"Z_c = \frac{{{p_hat:.4f} - {pi_0:.4f}}}{{\sqrt{{\frac{{{pi_0:.4f}(1-{pi_0:.4f})}}{{{total}}}}}}} = {z_calc:.4f}", "z_prueba_calc")
                
                st.write("**Paso 3: Región crítica**")
                st.write("Para una prueba bilateral con α = 0.05:")
                latex_copyable(rf"Z_{{\alpha/2}} = \pm {z_crit:.4f}", "z_critico")
                
                st.write("La región de rechazo es:")
                latex_copyable(rf"|Z_c| > Z_{{\alpha/2}} = {z_crit:.4f}", "region_rechazo")
                
                st.write("**Paso 4: Regla de decisión**")
                latex_copyable(r"\text{Rechazar } H_0 \text{ si } |Z_c| > Z_{\alpha/2}", "regla_decision")
                
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
                # Área de rechazo derecha
                x_rej_der = x[x >= z_crit]
                y_rej_der = stats.norm.pdf(x_rej_der)
                fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                                       fill='tozeroy', 
                                       name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                                       line=dict(color='red', width=0)))
                
                x_rej_izq = x[x <= -z_crit]
                y_rej_izq = stats.norm.pdf(x_rej_izq)
                fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                                       fill='tozeroy', 
                                       name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                                       line=dict(color='red', width=0)))
                
                # Agregar línea vertical para el valor calculado
                fig.add_vline(x=z_calc, 
                            line_dash="dash", 
                            line_color="green",
                            annotation_text=f"Z calc = {z_calc:.4f}",
                            annotation_position="top")
                
                # Actualizar layout
                fig.update_layout(
                    title='Distribución Normal Estándar',
                    xaxis_title='Z',
                    yaxis_title='Densidad',
                    showlegend=True
                )
                
                st.plotly_chart(fig)
                
                # Conclusión
                st.write("### Paso 5: Conclusión")
                if abs(z_calc) > z_crit:
                    st.write(f"""
                    Como |Z_c| = {abs(z_calc):.4f} > {z_crit:.4f}, se rechaza H₀.
                    
                    **Interpretación:**  
                    Con un nivel de confianza del 95%, existe evidencia estadística suficiente para concluir que 
                    la proporción de visitantes satisfechos es diferente del 75%.
                    """)
                else:
                    st.write(f"""
                    Como |Z_c| = {abs(z_calc):.4f} < {z_crit:.4f}, no se rechaza H₀.
                    
                    **Interpretación:**  
                    Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que la proporción
                    de visitantes satisfechos es diferente del 75%.
                    """)
                
                st.write(f"p-valor = {p_value:.4f}")
                
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
        
        **Hipótesis:**  
        - H₀: π₁ - π₂ = 0 (La proporción de satisfacción es igual en ambos géneros)
        - H₁: π₁ - π₂ ≠ 0 (Existe diferencia en la proporción de satisfacción entre géneros)
        
        **Tipo de Prueba:** Bilateral
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
            - Satisfechos (x₁) = {satisfechos_h}
            - Proporción (p₁) = {p1:.4f}
            
            **Grupo 2 (Mujeres):**
            - Tamaño de muestra (n₂) = {n2}
            - Satisfechas (x₂) = {satisfechos_m}
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
        
        # Fórmula del estadístico
        st.write("### Fórmula del Estadístico de Prueba")
        st.write("El estadístico de prueba es:")
        formula = r"Z_{cal} = \frac{p_1 - p_2 - (\pi_1 - \pi_2)}{\sqrt{\hat{p}(1-\hat{p})(\frac{1}{n_1} + \frac{1}{n_2})}}"
        latex_copyable(formula, "z_dif_prop")
        
        st.write("Donde la proporción combinada p̂ se calcula como:")
        formula = rf"\hat{{p}} = \frac{{x_1 + x_2}}{{n_1 + n_2}} = \frac{{{satisfechos_h} + {satisfechos_m}}}{{{n1} + {n2}}} = {p_comb:.4f}"
        latex_copyable(formula, "p_comb")

        st.write("Sustituyendo los valores:")
        numerador = f"{p1:.4f} - {p2:.4f}"
        denominador = f"{p_comb:.4f}(1-{p_comb:.4f})"
        formula = rf"Z_{{cal}} = \frac{{{numerador}}}{{\sqrt{{{denominador}}} \cdot \sqrt{{\frac{{1}}{{{n1}}} + \frac{{1}}{{{n2}}}}}}} = {z_calc:.4f}"
        latex_copyable(formula, "z_dif_prop_calc")
        
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
            Con un nivel de confianza del 95%, existe evidencia estadística suficiente para concluir que hay una 
            diferencia significativa en la proporción de visitantes satisfechos entre hombres y mujeres. 
            La diferencia observada de {abs(p1 - p2):.1%} puntos porcentuales es estadísticamente significativa.
            """)
        else:
            st.write(f"""
            Como el p-valor ({p_value:.4f}) es mayor que α ({alpha}), no se rechaza H₀.
            
            **Conclusión:**  
            Con un nivel de confianza del 95%, no existe evidencia estadística suficiente para concluir que hay una 
            diferencia significativa en la proporción de visitantes satisfechos entre hombres y mujeres. 
            La diferencia observada de {abs(p1 - p2):.1%} puntos porcentuales no es estadísticamente significativa.
            """)

    # 1.8 Varianza
    with pruebas_tabs[7]:
        st.write("## 1.8 Prueba de Hipótesis para la Varianza")
        
        st.write("""
        ### Ejemplo: Variabilidad en la Satisfacción
        
        **Contexto del Problema:**  
        El centro recreativo desea evaluar si la varianza de la satisfacción de sus visitantes 
        es diferente de 1 punto cuadrado. Con una varianza muestral de 0.9609 y n = 30 participantes. 
        Se desea determinar si existe evidencia estadística suficiente para concluir que la varianza 
        poblacional es diferente de 1, lo cual ayudaría a entender si la experiencia de los visitantes 
        es consistente o si hay una variabilidad significativa en sus niveles de satisfacción.
        
        **Planteamiento:**
        - Variable de estudio: Variabilidad en la satisfacción de los visitantes
        - Valor de referencia: σ² = 1 (varianza hipotética)
        - Varianza muestral: s² = 0.9609
        - Tamaño de muestra: n = 30
        - Nivel de significancia (α): 0.05
        
        **Hipótesis:**
        - H₀: σ² = 1 (La varianza poblacional es igual a 1)
        - H₁: σ² ≠ 1 (La varianza poblacional es diferente de 1)
        
        **Tipo de Prueba:** Bilateral
        """)
        
        # Cálculos
        n = len(df)
        s2 = df['Satisfaccion'].var()
        sigma2_0 = 1  # Varianza hipotética
        alpha = 0.05
        
        # Valores críticos (bilateral)
        chi2_crit_inf = stats.chi2.ppf(alpha/2, n - 1)
        chi2_crit_sup = stats.chi2.ppf(1 - alpha/2, n - 1)
        
        # Estadístico de prueba
        chi2_calc = (n - 1) * s2 / sigma2_0
        
        # P-valor (bilateral)
        if chi2_calc <= n - 1:
            p_value = 2 * stats.chi2.cdf(chi2_calc, n - 1)
        else:
            p_value = 2 * (1 - stats.chi2.cdf(chi2_calc, n - 1))
        
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
        
        # Área de rechazo izquierda
        x_rej_izq = x[x <= chi2_crit_inf]
        y_rej_izq = stats.chi2.pdf(x_rej_izq, n - 1)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Área de rechazo derecha
        x_rej_der = x[x >= chi2_crit_sup]
        y_rej_der = stats.chi2.pdf(x_rej_der, n - 1)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para chi2 calculado
        fig.add_vline(x=chi2_calc, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"χ² calc = {chi2_calc:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Hipótesis Bilateral para la Varianza de la Satisfacción',
            xaxis_title='Estadístico Chi-Cuadrado',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_hipotesis_varianza")
        
        # Resultados y fórmulas
        st.write("### Resultados")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"""
            **Datos:**
            - Tamaño de muestra (n) = {n}
            - Varianza muestral (s²) = {s2:.4f}
            - Varianza hipotética (σ₀²) = {sigma2_0}
            """)
            
        with col2:
            st.write(f"""
            **Estadísticos:**
            - χ² calculado = {chi2_calc:.4f}
            - χ² crítico inferior = {chi2_crit_inf:.4f}
            - χ² crítico superior = {chi2_crit_sup:.4f}
            - Valor p = {p_value:.4f}
            """)
        
        st.write("### Resolución Detallada")
        st.write("**1. Fórmula del Estadístico de Prueba:**")
        formula = r"\chi^2 = \frac{(n-1)S^2}{\sigma_0^2}"
        latex_copyable(formula, "chi_var")
        
        st.write("**2. Sustitución de Valores:**")
        st.write(f"""
        Donde:
        - n = {n} (tamaño de muestra)
        - S² = {s2:.4f} (varianza muestral)
        - σ₀² = {sigma2_0} (varianza hipotética)
        """)
        
        # Paso a paso
        st.write("**3. Desarrollo:**")
        paso1 = rf"\chi^2 = \frac{{({n}-1)({s2:.4f})}}{{{sigma2_0}}}"
        latex_copyable(paso1, "paso1")
        
        paso2 = rf"\chi^2 = \frac{{{n-1} \cdot {s2:.4f}}}{{{sigma2_0}}}"
        latex_copyable(paso2, "paso2")
        
        paso3 = rf"\chi^2 = \frac{{{(n-1)*s2:.4f}}}{{{sigma2_0}}} = {chi2_calc:.4f}"
        latex_copyable(paso3, "paso3")
        
        st.write("**4. Decisión:**")
        if chi2_calc < chi2_crit_inf or chi2_calc > chi2_crit_sup:
            st.write(f"""
            Como χ² = {chi2_calc:.4f} está fuera del intervalo [{chi2_crit_inf:.4f}, {chi2_crit_sup:.4f}], 
            se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del {(1-alpha)*100}%, existe evidencia estadística suficiente para concluir que 
            la varianza poblacional es diferente de {sigma2_0} unidades cuadradas.
            """)
        else:
            st.write(f"""
            Como χ² = {chi2_calc:.4f} está dentro del intervalo [{chi2_crit_inf:.4f}, {chi2_crit_sup:.4f}], 
            no se rechaza H₀.
            
            **Interpretación:**  
            Con un nivel de confianza del {(1-alpha)*100}%, no existe evidencia estadística suficiente para concluir que 
            la varianza poblacional es diferente de {sigma2_0} unidades cuadradas.
            """)
        
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
        
        # Datos fijos
        datos_fijos = {
            'Participante': list(range(1, 31)),
            'Satisfaccion': [5,5,4,5,2,4,4,4,4,5,4,4,4,4,4,5,4,4,4,2,5,2,4,5,2,5,4,4,2,4],
            'Racha': ['+','+','0','+','-','0','+','0','0','+','0','0','0','0','0','+','0','0','0','-','+','-','0','+','-','+','+','0','-','0']
        }
        
        df_rachas = pd.DataFrame(datos_fijos)
        
        # Mostrar información
        st.write("**Datos y Signos:**")
        st.write("Mediana de Satisfacción = 4.0")
        st.write(df_rachas)
        
        # Mostrar resultados
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
        r = min(n_pos, n_neg) if n_pos + n_neg > 0 else 0
        p_value = 2 * stats.binom.cdf(r, n_pos + n_neg, 0.5) if n_pos + n_neg > 0 else 1.0
        
        st.write(f"""
        **Paso 3: Cálculo del P-valor**
        - r (mínimo entre n⁺ y n⁻) = {r}
        - n efectivo = {n_pos + n_neg}
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
        mu = (n_pos + n_neg) * 0.5  # media bajo H0
        sigma = np.sqrt((n_pos + n_neg) * 0.5 * 0.5)  # desviación estándar bajo H0
        
        # Crear datos para la distribución normal
        x = np.linspace(-4, 4, 1000)
        y = stats.norm.pdf(x)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva normal
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Normal',
                               line=dict(color='blue')))
        
        # Áreas de rechazo
        # Área de rechazo derecha
        z_crit = 1.96
        z_calc = 3.2272
        alpha = 0.05
        
        x_rej_der = x[x >= z_crit]
        y_rej_der = stats.norm.pdf(x_rej_der)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {alpha/2:.3f})',
                               line=dict(color='red', width=0)))
        
        x_rej_izq = x[x <= -z_crit]
        y_rej_izq = stats.norm.pdf(x_rej_izq)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
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
        
        # Datos fijos
        datos = pd.DataFrame({
            'Participante': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
            'Satisfaccion': [5,5,4,5,2,4,4,4,4,5,4,4,4,4,4,5,4,4,4,2,5,2,4,5,2,5,4,4,2,4],
            'Racha': ['+','+','0','+','-','0','+','0','0','+','0','0','0','0','0','+','0','0','0','-','+','-','0','+','-','+','+','0','-','0']
        })
        
        # Mostrar tabla de datos
        st.write("**Datos y Signos:**")
        st.write("Mediana de Satisfacción = 4.0")
        st.dataframe(datos)
        
        # Mostrar resultados de la prueba
        st.write("### Prueba de Hipótesis")
        
        st.write("""
        **Paso 1: Plantear Hipótesis**
        - H₀: La secuencia es aleatoria
        - H₁: La secuencia no es aleatoria
        
        **Paso 2: Estadísticos**
        - Número de rachas (R) = 12
        - n₁ (≥ mediana) = 7
        - n₂ (< mediana) = 5
        - Z crítico = ±1.96
        """)
        
        st.write("### Resultados")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("""
            **Estadísticos calculados:**
            - Número esperado de rachas (E[R]): 6.8333
            - Varianza de las rachas (Var[R]): 2.5631
            - Valor calculado de z: 3.2272
            """)
        
        # Fórmulas en LaTeX
        st.write("### Fórmulas utilizadas")
        st.write("**Número esperado de rachas:**")
        latex_copyable(r"E[R] = 1 + \frac{2n_1n_2}{n_1 + n_2}", "formula_er")
        st.write("**Resolución E[R]:**")
        latex_copyable(r"E[R] = 1 + \frac{2(7)(5)}{7 + 5} = 1 + \frac{70}{12} = 6.8333", "rachas_er_resolucion")
        
        st.write("**Varianza de las rachas:**")
        latex_copyable(r"Var[R] = \frac{2n_1n_2(2n_1n_2 - n_1 - n_2)}{(n_1 + n_2)^2(n_1 + n_2 - 1)}", "formula_var")
        st.write("**Resolución Var[R]:**")
        latex_copyable(r"Var[R] = \frac{2(7)(5)(2(7)(5) - 7 - 5)}{(7 + 5)^2(7 + 5 - 1)} = \frac{70(70 - 12)}{144(11)} = 2.5631", "rachas_var_resolucion")
        
        st.write("**Estadístico Z:**")
        latex_copyable(r"Z = \frac{R - E[R]}{\sqrt{Var[R]}}", "formula_z")
        
        st.write("**Resolución:**")
        latex_copyable(r"Z = \frac{12 - 6.8333}{\sqrt{2.5631}} = 3.2272", "resolucion_z")
        
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
        # Área de rechazo izquierda
        x_rej_izq = x[x <= -1.96]
        y_rej_izq = stats.norm.pdf(x_rej_izq)
        fig.add_trace(go.Scatter(x=x_rej_izq, y=y_rej_izq, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {0.05/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Área de rechazo derecha
        x_rej_der = x[x >= 1.96]
        y_rej_der = stats.norm.pdf(x_rej_der)
        fig.add_trace(go.Scatter(x=x_rej_der, y=y_rej_der, 
                               fill='tozeroy', 
                               name=f'Región de Rechazo (α/2 = {0.05/2:.3f})',
                               line=dict(color='red', width=0)))
        
        # Agregar línea vertical para z calculado
        fig.add_vline(x=3.2272, 
                     line_dash="dash", 
                     line_color="green",
                     annotation_text=f"z calc = {3.2272:.4f}",
                     annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title='Prueba de Rachas',
            xaxis_title='Estadístico Z',
            yaxis_title='Densidad',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Interpretación
        st.write("### Conclusión")
        st.write("""
        |z| = 3.2272 > 1.96, se rechaza la hipótesis nula (H₀).
        
        **Conclusión:** Existe evidencia suficiente para afirmar que la secuencia NO es aleatoria.
        """)