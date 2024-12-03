import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

def latex_copyable(formula, label):
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
st.set_page_config(page_title="Análisis Inferencial", page_icon="🔍", layout="wide")

# JavaScript para copiar al portapapeles
st.markdown("""
<script>
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        console.log('Copying to clipboard was successful!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}
</script>
""", unsafe_allow_html=True)

# Función para cargar datos
@st.cache_data(ttl=0)  # ttl=0 significa que el caché se invalida en cada recarga
def cargar_datos():
    ruta_base = Path(__file__).parent.parent
    ruta_datos = ruta_base / 'data' / 'encuesta_recreacion_numerica.csv'
    df = pd.read_csv(ruta_datos)
    # Asegurarnos que Genero sea tipo int
    df['Genero'] = df['Genero'].astype(int)
    # Asegurarnos que Importancia_Costo sea tipo int
    df['Importancia_Costo'] = df['Importancia_Costo'].astype(int)
    return df

# Cargar datos
df = cargar_datos()

# Título principal
st.title("🔍 Análisis Inferencial")
st.write("Análisis estadístico inferencial de la encuesta de recreación")

# Crear tabs principales
tab1, tab2 = st.tabs(["6. Distribuciones Muestrales", "7. Intervalos de Confianza"])

with tab1:
    st.header("6. Distribuciones Muestrales")
    
    # Subtabs para cada tipo de distribución muestral
    dist_tabs = st.tabs([
        "a) Media (σ conocida)",
        "b) Media (σ desconocida)",
        "c) Diferencia Medias (σ conocida)",
        "d) Diferencia Medias (σ iguales)",
        "e) Diferencia Medias (σ diferentes)",
        "f) Proporción",
        "g) Diferencia Proporciones"
    ])
    
    # a) Media con Varianza Conocida
    with dist_tabs[0]:
        st.subheader("a) Distribución Muestral para la Media con Varianza Conocida")
        
        # Selección de variable
        variable = st.selectbox(
            "Seleccione la variable numérica a analizar:",
            ["Edad", "Frecuencia_Visitas", "Satisfaccion", "Preferencia"],
            key="var_normal"
        )
        
        # Calcular estadísticos
        datos_variable = df[variable].dropna()
        n = len(datos_variable)
        media = datos_variable.mean()
        std = datos_variable.std()
        
        # Planteamiento del problema
        st.write(f"""
        ### Planteamiento del Problema
        
        Se sabe que, en promedio, {media:.2f} es el valor de **{variable}** en el centro de recreación. 
        Estudios previos indican que la desviación estándar de este número es de {std:.2f}. 
        Se tiene una muestra de {n} personas.
        """)
        
        st.write("¿Cuál es la probabilidad de que la media de esa muestra:")
        
        # Valores a analizar
        valor1 = st.number_input(f"a) Sea mayor a:", value=float(media + std/2), step=0.1)
        valor2 = st.number_input(f"b) Sea menor a:", value=float(media - std/2), step=0.1)
        
        # Fórmula principal con botón de copiar
        st.write("### Fórmula:")
        latex_copyable(r"Z = \frac{\bar{X} - \mu}{\sigma/\sqrt{n}}", "principal")
        
        # Donde:
        st.write("""
        Donde:
        - X̄: Media muestral
        - μ: Media poblacional
        - σ: Desviación estándar poblacional
        - n: Tamaño de la muestra
        """)
        
        # Datos
        st.write("### Datos:")
        st.write(f"""
        σ = {std:.2f}
        μ = {media:.2f}
        n = {n}
        """)
        
        # Desarrollo a)
        st.write(f"### a) Sea mayor a {valor1}")
        latex_copyable(f"P(\\bar{{x}} > {valor1}) = 1 - P(\\bar{{x}} \\leq {valor1})", "prob_a1")
        
        st.write("Estandarizando:")
        z_score1 = (valor1 - media)/(std/np.sqrt(n))
        latex_copyable(f"P(\\bar{{x}} > {valor1}) = 1 - P(Z \\leq {z_score1:.2f})", "prob_a2")
        
        prob_mayor = 1 - stats.norm.cdf(z_score1)
        latex_copyable(f"P(\\bar{{x}} > {valor1}) = 1 - {1-prob_mayor:.5f}", "prob_a3")
        latex_copyable(f"P(\\bar{{x}} > {valor1}) = {prob_mayor:.5f}", "prob_a4")
        
        # Desarrollo b)
        st.write(f"### b) Sea menor a {valor2}")
        latex_copyable(f"P(\\bar{{x}} < {valor2})", "prob_b1")
        
        st.write("Estandarizando:")
        z_score2 = (valor2 - media)/(std/np.sqrt(n))
        latex_copyable(f"P(\\bar{{x}} < {valor2}) = P(Z < {z_score2:.2f})", "prob_b2")
        
        prob_menor = stats.norm.cdf(z_score2)
        latex_copyable(f"P(\\bar{{x}} < {valor2}) = {prob_menor:.5f}", "prob_b3")

        # Visualización
        fig = px.histogram(df, x=variable, nbins=20, title=f"Distribución de {variable}")
        fig.add_vline(x=valor1, line_dash="dash", line_color="red", annotation_text="Valor 1")
        fig.add_vline(x=valor2, line_dash="dash", line_color="blue", annotation_text="Valor 2")
        fig.add_vline(x=media, line_dash="solid", line_color="green", annotation_text="Media")
        st.plotly_chart(fig)
        
        # Interpretación
        st.write("### Interpretación:")
        st.write(f"""
        En ambos casos, las probabilidades de que la media se aleje del promedio ({media:.2f}) son:
        - Probabilidad de ser mayor a {valor1:.2f}: {prob_mayor*100:.2f}%
        - Probabilidad de ser menor a {valor2:.2f}: {prob_menor*100:.2f}%
        
        Esto refleja el comportamiento de la variable {variable} en el centro de recreación, 
        mostrando qué tan probable es obtener valores alejados de la media en futuras muestras.
        """)

    # b) Media con Varianza Desconocida (t-Student)
    with dist_tabs[1]:
        st.subheader("b) Distribución Muestral para la Media con Varianza Desconocida")
        
        # Selección de variable
        variable = st.selectbox(
            "Seleccione la variable numérica a analizar:",
            ["Edad", "Frecuencia_Visitas", "Satisfaccion", "Preferencia"],
            key="var_t"
        )
        
        # Diccionario de configuración por variable
        config_variables = {
            "Edad": {
                "unidad": "años",
                "periodo": "persona",
                "factor_variabilidad": "las características demográficas de los visitantes"
            },
            "Frecuencia_Visitas": {
                "unidad": "personas",
                "periodo": "día",
                "factor_variabilidad": "las condiciones de acceso y la oferta de servicios"
            },
            "Satisfaccion": {
                "unidad": "puntos",
                "periodo": "evaluación",
                "descripcion": "las experiencias individuales y servicios ofrecidos"
            },
            "Preferencia": {
                "unidad": "puntos",
                "periodo": "evaluación",
                "factor_variabilidad": "los gustos individuales y opciones disponibles"
            }
        }
        
        # Verificar datos antes de procesar
        st.write("### Verificación de Grupos")
        datos_variable = df[variable].dropna()
        n = len(datos_variable)
        
        if n < 2:
            st.error(f"""
            ⚠️ Error: No hay suficientes datos válidos para la variable {variable}.
            Se necesitan al menos 2 observaciones para calcular la desviación estándar.
            """)
            st.stop()
        
        # Calcular estadísticos reales
        media = datos_variable.mean()
        std = datos_variable.std()
        gl = n - 1  # Grados de libertad
        
        # Mostrar información de la muestra
        st.write(f"""
        ### Información de la Muestra
        
        Analizando la variable **{variable}**:
        - Número de participantes (n) = {n}
        - Grados de libertad (gl) = {gl}
        - Media muestral (x̄) = {media:.2f}
        - Desviación estándar muestral (s) = {std:.2f}
        """)
        
        # Generar contexto automático
        st.write("### Contexto del Análisis")
        contexto = f"""Se sabe que, en promedio, {variable.lower().replace('_', ' ')} es de {media:.1f} {config_variables[variable]['unidad']} por {config_variables[variable]['periodo']}. 
        Debido a la variabilidad en {config_variables[variable]['factor_variabilidad']}, no se conoce con precisión la desviación estándar.
        Sin embargo, una muestra aleatoria de {n} {config_variables[variable]['periodo']}s reveló una desviación estándar de {std:.1f} {config_variables[variable]['unidad']}."""
        
        st.write(contexto)
        
        # Fórmula principal con botón de copiar
        st.write("### Fórmula:")
        latex_copyable(r"t = \frac{\bar{X} - \mu_0}{s/\sqrt{n}}", "t_formula")
        
        # Explicación
        st.write("""
        Donde:
        - x̄ = Media muestral
        - μ₀ = Media poblacional hipotética
        - s = Desviación estándar muestral
        - n = Tamaño de la muestra
        """)
        
        # Valores a analizar
        st.write("### Análisis de Probabilidades")
        valor = st.number_input(
            "Valor de referencia para μ₀:",
            value=float(media),
            step=0.1,
            key="t_valor"
        )
        
        # Cálculo del estadístico t
        t_stat = (media - valor)/(std/np.sqrt(n))
        
        # Valores críticos
        t_crit_left = stats.t.ppf(0.025, gl)  # Punto crítico izquierdo (2.5%)
        t_crit_right = stats.t.ppf(0.975, gl)  # Punto crítico derecho (97.5%)
        
        # Probabilidades
        p_mayor = 1 - stats.t.cdf(t_stat, gl)
        p_menor = stats.t.cdf(t_stat, gl)
        p_bilateral = 2 * min(p_mayor, p_menor)
        
        # Mostrar resultados
        st.write("### Resultados")
        
        # Fórmula del cálculo
        latex_copyable(
            rf"t = \frac{{{media:.2f} - {valor}}}{{{std:.2f}/\sqrt{{{n}}}}} = {t_stat:.4f}",
            "t_calc"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"""
            #### Probabilidades:
            - P(diferencia > {valor}) = {p_mayor:.4f}
            - P(diferencia < {valor}) = {p_menor:.4f}
            - P(bilateral) = {p_bilateral:.4f}
            
            #### Valores Críticos (α = 0.05):
            - t₍₀.₀₂₅₎ = {t_crit_left:.4f}
            - t₍₀.₉₇₅₎ = {t_crit_right:.4f}
            """)
        
        with col2:
            # Visualización
            x = np.linspace(stats.t.ppf(0.001, gl), stats.t.ppf(0.999, gl), 100)
            y = stats.t.pdf(x, gl)
            
            # Crear figura
            fig = px.line(x=x, y=y)
            
            # Agregar línea vertical para el estadístico t calculado
            fig.add_vline(x=t_stat, line_dash="dash", line_color="red",
                         annotation_text="t calculado",
                         annotation_position="top")
            
            # Agregar líneas verticales para los puntos críticos
            fig.add_vline(x=t_crit_left, line_dash="dash", line_color="green",
                         annotation_text="t₍₀.₀₂₅₎",
                         annotation_position="bottom")
            fig.add_vline(x=t_crit_right, line_dash="dash", line_color="green",
                         annotation_text="t₍₀.₉₇₅₎",
                         annotation_position="bottom")
            
            # Agregar área sombreada para región crítica
            fig.add_scatter(x=x[x <= t_crit_left], y=y[x <= t_crit_left],
                          fill='tozeroy', fillcolor='rgba(255,0,0,0.2)',
                          line=dict(width=0), name='Región crítica',
                          showlegend=True)
            fig.add_scatter(x=x[x >= t_crit_right], y=y[x >= t_crit_right],
                          fill='tozeroy', fillcolor='rgba(255,0,0,0.2)',
                          line=dict(width=0), name='Región crítica',
                          showlegend=False)
            
            # Actualizar layout
            fig.update_layout(
                title="Distribución t-Student",
                xaxis_title="t",
                yaxis_title="Densidad",
                showlegend=True
            )
            st.plotly_chart(fig)
        
        # Interpretación
        st.write("### Interpretación:")
        
        if abs(t_stat) > abs(t_crit_right):
            interpretacion = f"""
            El valor del estadístico t ({t_stat:.4f}) cae en la región crítica 
            (|t| > {abs(t_crit_right):.4f}), lo que sugiere que hay evidencia estadística 
            significativa de que la media poblacional es diferente del valor de referencia 
            con un nivel de significancia de 0.05.
            
            La diferencia observada ({media-valor:.4f}) es estadísticamente significativa.
            """
        else:
            interpretacion = f"""
            El valor del estadístico t ({t_stat:.4f}) no cae en la región crítica 
            (|t| ≤ {abs(t_crit_right):.4f}), lo que sugiere que no hay evidencia estadística 
            significativa de que la media poblacional sea diferente del valor de referencia 
            con un nivel de significancia de 0.05.
            
            La diferencia observada ({media-valor:.4f}) no es estadísticamente significativa.
            """
        
        st.write(interpretacion)
        
        # Paso a paso
        with st.expander("Ver desarrollo paso a paso"):
            st.write("""
            1. **Identificación del problema**
               - Variable cuantitativa
               - Varianza poblacional desconocida
               - Se usa distribución t-Student
            
            2. **Cálculo de estadísticos muestrales**
               - Media muestral (x̄)
               - Desviación estándar muestral (s)
               - Tamaño de muestra (n)
               - Grados de libertad (gl = n-1)
            
            3. **Cálculo del estadístico t**
               - Diferencia de medias observada
               - Error estándar de la diferencia
               - Comparación con valores críticos
            
            4. **Interpretación**
               - Análisis de región crítica
               - Cálculo de probabilidades
               - Conclusión sobre la significancia estadística
            """)

    # c) Diferencia de Medias (Varianza Conocida)
    with dist_tabs[2]:
        st.subheader("c) Distribución Muestral para la Diferencia de Medias (Varianza Conocida)")
        
        # Selección de variables
        col1, col2 = st.columns(2)
        with col1:
            # Variable a analizar
            variable = st.selectbox(
                "Seleccione la variable numérica a analizar:",
                ["Edad", "Frecuencia_Visitas", "Satisfaccion", "Preferencia"],
                key="var_diff"
            )
            
        with col2:
            # Variable de agrupación
            grupo = st.selectbox(
                "Seleccione la variable para agrupar:",
                ["Genero", "Importancia_Costo"],
                key="grupo_diff"
            )
        
        # Verificar datos antes de procesar
        st.write("### Verificación de Grupos")
        grupo_counts = df[grupo].value_counts().sort_index()
        st.write(f"Distribución de {grupo}:")
        st.write(grupo_counts)
        
        # Permitir seleccionar los grupos a comparar
        col1, col2 = st.columns(2)
        with col1:
            grupo_valor1 = st.selectbox(
                "Seleccione el primer grupo:",
                sorted(df[grupo].unique()),
                key="grupo1"
            )
        with col2:
            grupo_valor2 = st.selectbox(
                "Seleccione el segundo grupo:",
                [x for x in sorted(df[grupo].unique()) if x != grupo_valor1],
                key="grupo2"
            )
        
        # Obtener grupos y verificar tamaños
        grupo1_data = df[df[grupo] == grupo_valor1][variable]
        grupo2_data = df[df[grupo] == grupo_valor2][variable]
        
        # Calcular estadísticos
        n1 = len(grupo1_data)
        n2 = len(grupo2_data)
        media1 = grupo1_data.mean()
        media2 = grupo2_data.mean()
        var1 = grupo1_data.var()
        var2 = grupo2_data.var()
        
        # Diccionario de configuración por variable
        config_variables = {
            "Edad": {
                "unidad": "años",
                "periodo": "mes",
                "descripcion": "la edad promedio"
            },
            "Frecuencia_Visitas": {
                "unidad": "visitas",
                "periodo": "mes",
                "descripcion": "el número medio de visitas"
            },
            "Satisfaccion": {
                "unidad": "puntos",
                "periodo": "mes",
                "descripcion": "el nivel medio de satisfacción"
            },
            "Preferencia": {
                "unidad": "puntos",
                "periodo": "mes",
                "descripcion": "el nivel medio de preferencia"
            }
        }
        
        # Mostrar información de la muestra
        st.write(f"""
        ### Información de la Muestra
        
        Total de registros en la encuesta: **{len(df)}**
        
        La variable **{variable}** está siendo comparada entre dos grupos según **{grupo}**:
        """)
        
        # Mostrar advertencia si hay problemas con los grupos
        if n1 < 2 or n2 < 2:
            st.error(f"""
            ⚠️ Error: Uno o ambos grupos tienen muy pocas observaciones:
            - Grupo 1 ({grupo_valor1}): {n1} observaciones
            - Grupo 2 ({grupo_valor2}): {n2} observaciones
            
            Se necesitan al menos 2 observaciones por grupo para calcular la desviación estándar.
            """)
            st.stop()
        
        # Planteamiento del problema
        st.write(f"""
        ### Planteamiento
        
        **Grupo 1 ({grupo_valor1}):**
        - Media (x̄₁) = {media1:.2f}
        - Varianza (σ₁²) = {var1:.2f}
        - Tamaño (n₁) = {n1}
        
        **Grupo 2 ({grupo_valor2}):**
        - Media (x̄₂) = {media2:.2f}
        - Varianza (σ₂²) = {var2:.2f}
        - Tamaño (n₂) = {n2}
        """)
        
        # Fórmula principal con botón de copiar
        st.write("### Fórmula:")
        latex_copyable(r"Z = \frac{(\bar{X}_1 - \bar{X}_2) - (\mu_1 - \mu_2)}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}", "z_formula")
        
        st.write("""
        Donde:
        - x̄₁, x̄₂ = Medias muestrales
        - μ₁, μ₂ = Medias poblacionales
        - σ₁², σ₂² = Varianzas poblacionales
        - n₁, n₂ = Tamaños de muestra
        """)
        
        # Valores a analizar
        st.write("### Análisis de Probabilidades")
        diff_ref = st.number_input(
            "Diferencia de referencia (μ₁ - μ₂):",
            value=0.0,
            step=0.1,
            key="diff_ref"
        )
        
        # Generar contexto automático
        contexto = f"""{config_variables[variable]['descripcion'].capitalize()} a los centros recreativos por personas del grupo {grupo_valor1} 
        es de {media1:.1f} {config_variables[variable]['unidad']} por {config_variables[variable]['periodo']}, 
        con una varianza de {var1:.1f}. Por otro lado, {config_variables[variable]['descripcion']} por personas del grupo {grupo_valor2} 
        es de {media2:.1f} {config_variables[variable]['unidad']} por {config_variables[variable]['periodo']}, 
        con una varianza de {var2:.1f}.

        Si tomamos una muestra aleatoria de {n1} personas del grupo {grupo_valor1} y {n2} personas del grupo {grupo_valor2}, 
        ¿cuál es la probabilidad de que {config_variables[variable]['descripcion']} del grupo {grupo_valor1} sea al menos 
        {diff_ref:.1f} {config_variables[variable]['unidad']} mayor que {config_variables[variable]['descripcion']} del grupo {grupo_valor2}?"""
        
        st.write(contexto)
        
        # Cálculo del estadístico Z
        z_stat = ((media1 - media2) - diff_ref) / np.sqrt((var1/n1) + (var2/n2))
        
        # Valores críticos
        z_crit_left = stats.norm.ppf(0.025)
        z_crit_right = stats.norm.ppf(0.975)
        
        # Probabilidades
        p_mayor = 1 - stats.norm.cdf(z_stat)
        p_menor = stats.norm.cdf(z_stat)
        p_bilateral = 2 * min(p_mayor, p_menor)
        
        # Mostrar resultados
        st.write("### Resultados")
        
        # Fórmula del cálculo
        latex_copyable(
            rf"Z = \frac{{({media1:.2f} - {media2:.2f}) - {diff_ref}}}{{\sqrt{{\frac{{{var1:.2f}}}{{{n1}}} + \frac{{{var2:.2f}}}{{{n2}}}}}}} = {z_stat:.4f}",
            "z_calc"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"""
            #### Probabilidades:
            - P(diferencia > {diff_ref}) = {p_mayor:.4f}
            - P(diferencia < {diff_ref}) = {p_menor:.4f}
            - P(bilateral) = {p_bilateral:.4f}
            
            #### Valores Críticos (α = 0.05):
            - Z₍₀.₀₂₅₎ = {z_crit_left:.4f}
            - Z₍₀.₉₇₅₎ = {z_crit_right:.4f}
            """)
        
        with col2:
            # Visualización
            x = np.linspace(-4, 4, 100)
            y = stats.norm.pdf(x)
            
            # Crear figura
            fig = px.line(x=x, y=y)
            
            # Agregar línea vertical para el estadístico Z calculado
            fig.add_vline(x=z_stat, line_dash="dash", line_color="red",
                         annotation_text="Z calculado",
                         annotation_position="top")
            
            # Agregar líneas verticales para los puntos críticos
            fig.add_vline(x=z_crit_left, line_dash="dash", line_color="green",
                         annotation_text="Z₍₀.₀₂₅₎",
                         annotation_position="bottom")
            fig.add_vline(x=z_crit_right, line_dash="dash", line_color="green",
                         annotation_text="Z₍₀.₉₇₅₎",
                         annotation_position="bottom")
            
            # Agregar área sombreada para región crítica
            fig.add_scatter(x=x[x <= z_crit_left], y=y[x <= z_crit_left],
                          fill='tozeroy', fillcolor='rgba(255,0,0,0.2)',
                          line=dict(width=0), name='Región crítica',
                          showlegend=True)
            fig.add_scatter(x=x[x >= z_crit_right], y=y[x >= z_crit_right],
                          fill='tozeroy', fillcolor='rgba(255,0,0,0.2)',
                          line=dict(width=0), name='Región crítica',
                          showlegend=False)
            
            # Actualizar layout
            fig.update_layout(
                title="Distribución Normal Estándar",
                xaxis_title="Z",
                yaxis_title="Densidad",
                showlegend=True
            )
            st.plotly_chart(fig)
        
        # Interpretación
        st.write("### Interpretación:")
        
        if abs(z_stat) > abs(z_crit_right):
            interpretacion = f"""
            El valor del estadístico Z ({z_stat:.4f}) cae en la región crítica 
            (|Z| > {abs(z_crit_right):.4f}), lo que sugiere que hay evidencia estadística 
            significativa de que existe una diferencia entre las medias poblacionales de los dos grupos
            con un nivel de significancia de 0.05.
            
            La diferencia observada ({media1-media2:.4f}) es estadísticamente significativa.
            """
        else:
            interpretacion = f"""
            El valor del estadístico Z ({z_stat:.4f}) no cae en la región crítica 
            (|Z| ≤ {abs(z_crit_right):.4f}), lo que sugiere que no hay evidencia estadística 
            significativa de que exista una diferencia entre las medias poblacionales de los dos grupos
            con un nivel de significancia de 0.05.
            
            La diferencia observada ({media1-media2:.4f}) no es estadísticamente significativa.
            """
        
        st.write(interpretacion)
        
        # Paso a paso
        with st.expander("Ver desarrollo paso a paso"):
            st.write("""
            1. **Identificación del problema**
               - Comparación de dos grupos independientes
               - Variable cuantitativa
               - Varianzas poblacionales conocidas
            
            2. **Cálculo de estadísticos por grupo**
               - Medias muestrales
               - Desviaciones estándar
               - Tamaños de muestra
            
            3. **Cálculo del estadístico Z**
               - Diferencia de medias observada
               - Error estándar de la diferencia
               - Comparación con valores críticos
            
            4. **Interpretación**
               - Análisis de región crítica
               - Cálculo de probabilidades
               - Conclusión sobre la significancia estadística
            """)

    # f) Proporción
    with dist_tabs[5]:
        st.write("## f) Distribución Muestral para Proporciones")
        
        st.write("""
        Esta sección permite analizar la distribución muestral de proporciones. 
        Es útil cuando queremos hacer inferencias sobre proporciones poblacionales basadas en datos muestrales.
        """)
        
        # Entrada de datos
        col1, col2 = st.columns(2)
        
        # Calcular valores por defecto basados en datos reales
        satisfaccion_alta = 4  # Definimos satisfacción alta como ≥4
        total_satisfechos = sum(df['Satisfaccion'] >= satisfaccion_alta)
        total_visitantes = len(df)
        
        with col1:
            # Proporción poblacional
            num_exitos = st.number_input(
                "Número de visitantes satisfechos (≥4):",
                min_value=0,
                value=total_satisfechos,
                step=1,
                key="num_exitos"
            )
            tam_poblacion = st.number_input(
                "Total de visitantes:",
                min_value=1,
                value=total_visitantes,
                step=1,
                key="tam_poblacion"
            )
            
        with col2:
            # Tamaño de muestra
            n = st.number_input(
                "Tamaño de la muestra:",
                min_value=1,
                value=min(50, total_visitantes),  # Usar 50 o el total si es menor
                step=1,
                key="tam_muestra_prop"
            )
            # Proporción de referencia
            proporcion_actual = total_satisfechos / total_visitantes
            p_ref = st.number_input(
                "Proporción de referencia:",
                min_value=0.0,
                max_value=1.0,
                value=round(proporcion_actual, 2),  # Redondear a 2 decimales
                step=0.01,
                key="prop_ref"
            )
        
        # Cálculos básicos
        pi = num_exitos / tam_poblacion
        q = 1 - pi
        
        # Verificar condiciones
        if n <= 0:
            st.error("El tamaño de la muestra debe ser mayor que 0")
            st.stop()
        if pi <= 0 or pi >= 1:
            st.error("La proporción poblacional debe estar entre 0 y 1")
            st.stop()
            
        # Mostrar información básica
        st.write("### Información del Problema")
        st.write(f"""
        **Datos de la Población:**
        - Número de éxitos: {num_exitos}
        - Tamaño de la población: {tam_poblacion}
        - Proporción poblacional (π): {pi:.4f}
        - Complemento (1-π): {q:.4f}
        
        **Datos de la Muestra:**
        - Tamaño de muestra (n): {n}
        - Proporción de referencia: {p_ref:.4f}
        """)
        
        # Generar contexto automático
        contexto = f"""Se tiene conocimiento que {num_exitos} de {tam_poblacion} visitantes están satisfechos 
        con las instalaciones del centro recreativo. Se recopila una muestra de {n} visitantes. 
        Calcular la probabilidad de que la proporción de visitantes satisfechos con las instalaciones 
        sea mayor al {p_ref:.1%}."""
        
        st.write(contexto)
        
        # Fórmula principal
        st.write("### Fórmula:")
        latex_copyable(r"Z = \frac{\hat{p} - \pi}{\sqrt{\frac{\pi(1-\pi)}{n}}}", "z_prop_formula")
        
        st.write("""
        Donde:
        - π = Proporción poblacional
        - p̂ = Proporción muestral de referencia
        - n = Tamaño de la muestra
        """)
        
        # Cálculos
        error_std = np.sqrt((pi * q) / n)
        z_stat = (p_ref - pi) / error_std
        
        # Probabilidades
        p_mayor = 1 - stats.norm.cdf(z_stat)
        p_menor = stats.norm.cdf(z_stat)
        p_bilateral = 2 * min(p_mayor, p_menor)
        
        # Valores críticos
        z_crit_left = stats.norm.ppf(0.025)
        z_crit_right = stats.norm.ppf(0.975)
        
        # Mostrar resultados
        st.write("### Resultados")
        
        # Fórmula del cálculo
        latex_copyable(
            rf"Z = \frac{{{p_ref:.4f} - {pi:.4f}}}{{\sqrt{{\frac{{{pi:.4f}(1-{pi:.4f})}}{{{n}}}}}}} = {z_stat:.4f}",
            "z_calc_prop"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"""
            #### Probabilidades:
            - P(p̂ > {p_ref}) = {p_mayor:.4f}
            - P(p̂ < {p_ref}) = {p_menor:.4f}
            - P(bilateral) = {p_bilateral:.4f}
            
            #### Valores Críticos (α = 0.05):
            - Z₍₀.₀₂₅₎ = {z_crit_left:.4f}
            - Z₍₀.₉₇₅₎ = {z_crit_right:.4f}
            """)
        
        with col2:
            # Visualización
            x = np.linspace(-4, 4, 100)
            y = stats.norm.pdf(x)
            
            # Crear figura
            fig = px.line(x=x, y=y)
            
            # Agregar línea vertical para el estadístico Z calculado
            fig.add_vline(x=z_stat, line_dash="dash", line_color="red",
                         annotation_text="Z calculado",
                         annotation_position="top")
            
            # Agregar líneas verticales para los puntos críticos
            fig.add_vline(x=z_crit_left, line_dash="dash", line_color="green",
                         annotation_text="Z₍₀.₀₂₅₎",
                         annotation_position="bottom")
            fig.add_vline(x=z_crit_right, line_dash="dash", line_color="green",
                         annotation_text="Z₍₀.₉₇₅₎",
                         annotation_position="bottom")
            
            # Agregar área sombreada para región crítica
            fig.add_scatter(x=x[x <= z_crit_left], y=y[x <= z_crit_left],
                          fill='tozeroy', fillcolor='rgba(255,0,0,0.2)',
                          line=dict(width=0), name='Región crítica',
                          showlegend=True)
            fig.add_scatter(x=x[x >= z_crit_right], y=y[x >= z_crit_right],
                          fill='tozeroy', fillcolor='rgba(255,0,0,0.2)',
                          line=dict(width=0), name='Región crítica',
                          showlegend=False)
            
            # Actualizar layout
            fig.update_layout(
                title="Distribución Normal Estándar",
                xaxis_title="Z",
                yaxis_title="Densidad",
                showlegend=True
            )
            st.plotly_chart(fig)
        
        # Interpretación
        st.write("### Interpretación:")
        
        if abs(z_stat) > abs(z_crit_right):
            interpretacion = f"""
            El valor del estadístico Z ({z_stat:.4f}) cae en la región crítica 
            (|Z| > {abs(z_crit_right):.4f}), lo que sugiere que hay evidencia estadística 
            significativa de que la proporción poblacional es diferente de {p_ref:.4f}
            con un nivel de significancia de 0.05.
            
            La probabilidad de observar una proporción mayor que {p_ref:.4f} es {p_mayor:.4f} ({p_mayor*100:.1f}%).
            """
        else:
            interpretacion = f"""
            El valor del estadístico Z ({z_stat:.4f}) no cae en la región crítica 
            (|Z| ≤ {abs(z_crit_right):.4f}), lo que sugiere que no hay evidencia estadística 
            significativa de que la proporción poblacional sea diferente de {p_ref:.4f}
            con un nivel de significancia de 0.05.
            
            La probabilidad de observar una proporción mayor que {p_ref:.4f} es {p_mayor:.4f} ({p_mayor*100:.1f}%).
            """
        
        st.write(interpretacion)

    # g) Diferencia de Proporciones
    with dist_tabs[6]:
        st.write("## g) Distribución Muestral para Diferencia de Proporciones")
        
        st.write("""
        Esta sección analiza la diferencia entre las proporciones de satisfacción alta (≥4) entre hombres y mujeres.
        """)
        
        # Calcular proporciones y tamaños de muestra por género
        satisfaccion_alta = 4  # Definimos satisfacción alta como ≥4
        
        # Grupo 1: Masculino (Género = 1)
        grupo1 = df[df['Genero'] == 1]
        n1 = len(grupo1)
        satisfechos1 = sum(grupo1['Satisfaccion'] >= satisfaccion_alta)
        p1 = satisfechos1 / n1
        
        # Grupo 2: Femenino (Género = 2)
        grupo2 = df[df['Genero'] == 2]
        n2 = len(grupo2)
        satisfechos2 = sum(grupo2['Satisfaccion'] >= satisfaccion_alta)
        p2 = satisfechos2 / n2
            
        # Mostrar información básica
        st.write("### Información del Problema")
        st.write(f"""
        **Grupo 1 (Masculino):**
        - Proporción (p₁): {p1:.4f}
        - Tamaño de muestra (n₁): {n1}
        - Complemento (1-p₁): {1-p1:.4f}
        
        **Grupo 2 (Femenino):**
        - Proporción (p₂): {p2:.4f}
        - Tamaño de muestra (n₂): {n2}
        - Complemento (1-p₂): {1-p2:.4f}
        """)
        
        # Generar contexto automático
        st.write("### Contexto del Análisis")
        contexto = f"""En nuestro estudio de satisfacción del centro recreativo, 
        se analizaron las respuestas de {n1} hombres y {n2} mujeres. El porcentaje de personas que 
        expresan alta satisfacción (≥4) es del {p1:.1%} en hombres y {p2:.1%} en mujeres. Analizaremos 
        si existe una diferencia significativa entre estas proporciones."""
        st.write(contexto)
        
        # Fórmula principal
        st.write("### Fórmula:")
        latex_copyable(r"Z = \frac{(p_1 - p_2) - (\pi_1 - \pi_2)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}", "z_prop_diff_formula")
        
        st.write("""
        Donde:
        - p₁, p₂ = Proporciones muestrales de satisfacción alta
        - π₁, π₂ = Proporciones poblacionales (asumimos π₁ = π₂)
        - n₁, n₂ = Tamaños de muestra por género
        """)
        
        # Cálculos
        error_std = np.sqrt((p1*(1-p1)/n1) + (p2*(1-p2)/n2))
        z_stat = (p1 - p2) / error_std
        
        # Probabilidades
        p_mayor = 1 - stats.norm.cdf(z_stat)
        p_menor = stats.norm.cdf(z_stat)
        p_bilateral = 2 * min(p_mayor, p_menor)
        
        # Valores críticos
        z_crit_left = stats.norm.ppf(0.025)
        z_crit_right = stats.norm.ppf(0.975)
        
        # Mostrar resultados
        st.write("### Resultados")
        
        # Fórmula del cálculo
        latex_copyable(
            rf"Z = \frac{{{p1:.4f} - {p2:.4f}}}{{\sqrt{{\frac{{{p1:.4f}(1-{p1:.4f})}}{{{n1}}} + \frac{{{p2:.4f}(1-{p2:.4f})}}{{{n2}}}}}}} = {z_stat:.4f}",
            "z_calc_prop_diff"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"""
            #### Probabilidades:
            - P(p₁ - p₂ > 0) = {p_mayor:.4f}
            - P(p₁ - p₂ < 0) = {p_menor:.4f}
            - P(bilateral) = {p_bilateral:.4f}
            
            #### Valores Críticos (α = 0.05):
            - Z₍₀.₀₂₅₎ = {z_crit_left:.4f}
            - Z₍₀.₉₇₅₎ = {z_crit_right:.4f}
            """)
        
        with col2:
            # Visualización
            x = np.linspace(-4, 4, 100)
            y = stats.norm.pdf(x)
            
            # Crear figura
            fig = px.line(x=x, y=y)
            
            # Agregar línea vertical para el estadístico Z calculado
            fig.add_vline(x=z_stat, line_dash="dash", line_color="red",
                         annotation_text="Z calculado",
                         annotation_position="top")
            
            # Agregar líneas verticales para los puntos críticos
            fig.add_vline(x=z_crit_left, line_dash="dash", line_color="green",
                         annotation_text="Z₍₀.₀₂₅₎",
                         annotation_position="bottom")
            fig.add_vline(x=z_crit_right, line_dash="dash", line_color="green",
                         annotation_text="Z₍₀.₉₇₅₎",
                         annotation_position="bottom")
            
            # Agregar área sombreada para región crítica
            fig.add_scatter(x=x[x <= z_crit_left], y=y[x <= z_crit_left],
                          fill='tozeroy', fillcolor='rgba(255,0,0,0.2)',
                          line=dict(width=0), name='Región crítica',
                          showlegend=True)
            fig.add_scatter(x=x[x >= z_crit_right], y=y[x >= z_crit_right],
                          fill='tozeroy', fillcolor='rgba(255,0,0,0.2)',
                          line=dict(width=0), name='Región crítica',
                          showlegend=False)
            
            # Actualizar layout
            fig.update_layout(
                title="Distribución Normal Estándar",
                xaxis_title="Z",
                yaxis_title="Densidad",
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Interpretación
        st.write("### Interpretación:")
        
        if abs(z_stat) > abs(z_crit_right):
            interpretacion = f"""
            El valor del estadístico Z ({z_stat:.4f}) cae en la región crítica 
            (|Z| > {abs(z_crit_right):.4f}), lo que sugiere que hay evidencia estadística 
            significativa de que existe una diferencia entre las proporciones de satisfacción alta
            entre hombres y mujeres, con un nivel de significancia de 0.05.
            
            La probabilidad de que la proporción de satisfacción alta en hombres sea mayor que en mujeres 
            es {p_mayor:.4f} ({p_mayor*100:.1f}%).
            """
        else:
            interpretacion = f"""
            El valor del estadístico Z ({z_stat:.4f}) no cae en la región crítica 
            (|Z| ≤ {abs(z_crit_right):.4f}), lo que sugiere que no hay evidencia estadística 
            significativa de que exista una diferencia entre las proporciones de satisfacción alta
            entre hombres y mujeres, con un nivel de significancia de 0.05.
            
            La probabilidad de que la proporción de satisfacción alta en hombres sea mayor que en mujeres 
            es {p_mayor:.4f} ({p_mayor*100:.1f}%).
            """
        
        st.write(interpretacion)
        
with tab2:
    st.header("7. Intervalos de Confianza")
    
    # Crear tabs para cada tipo de intervalo
    conf_tabs = st.tabs([
        "a) Media (σ² conocida)",
        "b) Media (σ² desconocida)",
        "c) Diferencia de Medias (σ² conocida)",
        "f) Proporción",
        "g) Diferencia de Proporciones",
        "h) Varianza"
    ])
    
    # a) Intervalo para la media con varianza conocida
    with conf_tabs[0]:
        st.write("## 7.1 Intervalo de Confianza para la Media (Varianza Conocida)")
        
        # Inputs para el usuario
        col1, col2 = st.columns(2)
        
        with col1:
            # Selección de variable
            var_ic_media = st.selectbox(
                "Seleccione la variable numérica",
                options=["Edad", "Frecuencia_Visitas", "Satisfaccion", "Preferencia"],
                key="var_ic_media"
            )
            
            # Calcular estadísticos de la variable seleccionada
            datos_var = df[var_ic_media]
            n_ic = len(datos_var)  # Tamaño de muestra
            media_muestral = datos_var.mean()  # Media muestral
            
            # Input para la desviación estándar poblacional
            desv_est = st.number_input(
                "Desviación estándar poblacional (σ)",
                min_value=0.1,
                value=datos_var.std(),  # Valor sugerido: desviación muestral
                step=0.1,
                key="desv_est_ic"
            )
            
            # Mostrar estadísticos calculados
            st.write("### Estadísticos Calculados:")
            st.write(f"""
            - Tamaño de muestra (n): {n_ic}
            - Media muestral (x̄): {media_muestral:.2f}
            """)
            
        with col2:
            # Nivel de confianza
            nivel_conf = st.slider(
                "Nivel de confianza",
                min_value=0.80,
                max_value=0.99,
                value=0.95,
                step=0.01,
                key="nivel_conf_ic_dist"
            )
        
        # Cálculos
        alpha = 1 - nivel_conf
        z_value = stats.norm.ppf(1 - alpha/2)
        error_est = z_value * (desv_est / np.sqrt(n_ic))
        
        ic_lower = media_muestral - error_est
        ic_upper = media_muestral + error_est
        
        # Mostrar información del problema
        st.write("### Información del Problema")
        st.write(f"""
        **Datos de la Variable '{var_ic_media}':**
        - Desviación estándar poblacional (σ): {desv_est:.2f}
        - Tamaño de muestra (n): {n_ic}
        - Media muestral (x̄): {media_muestral:.2f}
        - Nivel de confianza: {nivel_conf:.0%}
        """)
        
        # Generar contexto automático
        contexto = f"""Se analiza la variable '{var_ic_media}' de la encuesta de recreación. 
        A partir de una muestra de {n_ic} observaciones, se obtuvo una media muestral de {media_muestral:.2f} 
        y una desviación estándar poblacional de {desv_est:.2f}. Se desea construir un intervalo de confianza 
        al {nivel_conf:.0%} para la media poblacional."""
        st.write(contexto)
        
        # Fórmula
        st.write("### Fórmula:")
        latex_copyable(r"IC = \bar{x} \pm Z_{1-\frac{\alpha}{2}} \frac{\sigma}{\sqrt{n}}", "ic_media_formula")
        
        # Resolución de la fórmula
        st.write("### Resolución de la Fórmula:")
        latex_copyable(f"IC = {media_muestral:.4f} \pm {z_value:.4f} \\frac{{{desv_est:.4f}}}{{\sqrt{{{n_ic}}}}}", "ic_media_resolucion_1")
        latex_copyable(f"IC = {media_muestral:.4f} \pm {z_value:.4f} \\times {desv_est/np.sqrt(n_ic):.4f}", "ic_media_resolucion_2")
        latex_copyable(f"IC = {media_muestral:.4f} \pm {error_est:.4f}", "ic_media_resolucion_3")
        latex_copyable(f"IC = [{ic_lower:.4f}, {ic_upper:.4f}]", "ic_media_resolucion_4")

        # Cálculos intermedios
        st.write("### Cálculos:")
        st.write(f"""
        1. Valor crítico Z:
        - α = {alpha:.3f}
        - Z₍₁₋α/₂₎ = {z_value:.4f}
        
        2. Error estándar:
        - SE = {z_value:.4f} × ({desv_est:.2f}/√{n_ic})
        - SE = {error_est:.4f}
        """)
        
        # Resultado del intervalo
        st.write("### Intervalo de Confianza:")
        st.write(f"IC = {media_muestral:.2f} ± {error_est:.2f}")
        st.write(f"IC = [{ic_lower:.2f}, {ic_upper:.2f}]")
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución normal
        x = np.linspace(media_muestral - 4*desv_est/np.sqrt(n_ic), 
                       media_muestral + 4*desv_est/np.sqrt(n_ic), 1000)
        y = stats.norm.pdf(x, media_muestral, desv_est/np.sqrt(n_ic))
        
        # Crear el gráfico con plotly
        fig = go.Figure()
        
        # Agregar la curva normal completa
        fig.add_trace(go.Scatter(x=x, y=y, 
                               name='Distribución Normal',
                               line=dict(color='blue', width=2),
                               showlegend=True))
        
        # Agregar el área del intervalo de confianza
        x_ic = np.linspace(ic_lower, ic_upper, 1000)
        y_ic = stats.norm.pdf(x_ic, media_muestral, desv_est/np.sqrt(n_ic))
        fig.add_trace(go.Scatter(x=x_ic, y=y_ic, 
                               fill='tozeroy', 
                               name=f'Intervalo de Confianza {nivel_conf:.0%}',
                               line=dict(color='green', width=0),
                               fillcolor='rgba(0, 255, 0, 0.3)',
                               showlegend=True))
        
        # Agregar líneas verticales para los puntos críticos
        for punto in [ic_lower, ic_upper]:
            fig.add_vline(x=punto, 
                         line_dash="dash", 
                         line_color="red",
                         annotation_text=f"{punto:.2f}",
                         annotation_position="top")
        
        # Agregar línea vertical para la media
        fig.add_vline(x=media_muestral,
                     line_color="green",
                     annotation_text=f"Media: {media_muestral:.2f}",
                     annotation_position="top")
        
        # Personalizar el diseño
        fig.update_layout(
            title=f'Intervalo de Confianza para la Media de {var_ic_media} ({nivel_conf:.0%})',
            xaxis_title=var_ic_media,
            yaxis_title='Densidad',
            showlegend=True,
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            annotations=[
                dict(x=media_muestral, y=max(y)*1.1,
                     text=f"IC: [{ic_lower:.2f}, {ic_upper:.2f}]",
                     showarrow=False)
            ]
        )
        
        st.plotly_chart(fig)
        
        # Interpretación
        st.write("### Interpretación:")
        
        st.write(f"""Con un nivel de confianza del {nivel_conf:.0%}, se estima que la media poblacional 
        de la variable '{var_ic_media}' se encuentra entre {ic_lower:.2f} y {ic_upper:.2f}. 
        Esto significa que si tomáramos muchas muestras del mismo tamaño, aproximadamente el {nivel_conf:.0%} 
        de los intervalos calculados contendrían la verdadera media poblacional.""")

    # b) Intervalo para la media con varianza desconocida
    with conf_tabs[1]:
        st.write("## 7.2 Intervalo de Confianza para la Media (Varianza Desconocida)")
        
        # Inputs para el usuario
        col1, col2 = st.columns(2)
        with col1:
            # Selección de variable
            var_ic_media_t = st.selectbox(
                "Seleccione la variable numérica",
                options=["Edad", "Frecuencia_Visitas", "Satisfaccion", "Preferencia"],
                key="var_ic_media_t"
            )
            
            # Calcular estadísticos de la variable seleccionada
            datos_var = df[var_ic_media_t]
            n_ic = len(datos_var)  # Tamaño de muestra
            media_muestral = datos_var.mean()  # Media muestral
            desv_est_muestral = datos_var.std()  # Desviación estándar muestral
            grados_libertad = n_ic - 1  # Grados de libertad
            
            # Mostrar estadísticos calculados
            st.write("### Estadísticos Calculados:")
            st.write(f"""
            - Tamaño de muestra (n): {n_ic}
            - Media muestral (x̄): {media_muestral:.2f}
            - Desviación estándar muestral (s): {desv_est_muestral:.2f}
            - Grados de libertad (n-1): {grados_libertad}
            """)
            
        with col2:
            # Nivel de confianza
            nivel_conf = st.slider(
                "Nivel de confianza",
                min_value=0.80,
                max_value=0.99,
                value=0.95,
                step=0.01,
                key="nivel_conf_ic_t_dist"
            )
        
        # Cálculos
        alpha = 1 - nivel_conf
        t_value = stats.t.ppf(1 - alpha/2, grados_libertad)  # Valor t de Student
        error_est = t_value * (desv_est_muestral / np.sqrt(n_ic))
        
        ic_lower = media_muestral - error_est
        ic_upper = media_muestral + error_est
        
        # Mostrar información del problema
        st.write("### Información del Problema")
        st.write(f"""
        **Datos de la Variable '{var_ic_media_t}':**
        - Tamaño de muestra (n): {n_ic}
        - Media muestral (x̄): {media_muestral:.2f}
        - Desviación estándar muestral (s): {desv_est_muestral:.2f}
        - Nivel de confianza: {nivel_conf:.0%}
        - Valor t₍{grados_libertad}₎: {t_value:.4f}
        """)
        
        # Generar contexto automático
        st.write("### Contexto del Análisis")
        contexto = f"""Se analiza la variable '{var_ic_media_t}' de la encuesta de recreación. 
        A partir de una muestra de {n_ic} observaciones, se obtuvo una media muestral de {media_muestral:.2f} 
        y una desviación estándar muestral de {desv_est_muestral:.2f}. Como la varianza poblacional es desconocida, 
        se utiliza la distribución t de Student con {grados_libertad} grados de libertad para construir un 
        intervalo de confianza al {nivel_conf:.0%} para la media poblacional."""
        st.write(contexto)
        
        # Fórmula
        st.write("### Fórmula:")
        latex_copyable(r"IC = \bar{x} \pm t_{n-1,1-\frac{\alpha}{2}} \frac{s}{\sqrt{n}}", "ic_media_t_formula")
        
        # Resolución de la fórmula
        st.write("### Resolución de la Fórmula:")
        latex_copyable(f"IC = {media_muestral:.4f} \pm {t_value:.4f} \\frac{{{desv_est_muestral:.4f}}}{{\sqrt{{{n_ic}}}}}", "ic_media_t_resolucion_1")
        latex_copyable(f"IC = {media_muestral:.4f} \pm {t_value:.4f} \\times {desv_est_muestral/np.sqrt(n_ic):.4f}", "ic_media_t_resolucion_2")
        latex_copyable(f"IC = {media_muestral:.4f} \pm {error_est:.4f}", "ic_media_t_resolucion_3")
        latex_copyable(f"IC = [{ic_lower:.4f}, {ic_upper:.4f}]", "ic_media_t_resolucion_4")

        # Cálculos intermedios
        st.write("### Cálculos:")
        st.write(f"""
        1. Valor crítico t:
        - α = {alpha:.3f}
        - t₍{grados_libertad}₎ = {t_value:.4f}
        
        2. Error estándar:
        - SE = {t_value:.4f} × ({desv_est_muestral:.2f}/√{n_ic})
        - SE = {error_est:.4f}
        """)
        
        # Resultado del intervalo
        st.write("### Intervalo de Confianza:")
        st.write(f"IC = {media_muestral:.2f} ± {error_est:.2f}")
        st.write(f"IC = [{ic_lower:.2f}, {ic_upper:.2f}]")
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución t
        x = np.linspace(media_muestral - 4*desv_est_muestral/np.sqrt(n_ic), 
                       media_muestral + 4*desv_est_muestral/np.sqrt(n_ic), 1000)
        y = stats.t.pdf(x, grados_libertad, loc=media_muestral, 
                       scale=desv_est_muestral/np.sqrt(n_ic))
        
        # Crear el gráfico con plotly
        fig = go.Figure()
        
        # Agregar la curva t de Student
        fig.add_trace(go.Scatter(x=x, y=y, 
                               name='Distribución t-Student',
                               line=dict(color='blue', width=2),
                               showlegend=True))
        
        # Agregar el área del intervalo de confianza
        x_ic = np.linspace(ic_lower, ic_upper, 1000)
        y_ic = stats.t.pdf(x_ic, grados_libertad, loc=media_muestral, 
                          scale=desv_est_muestral/np.sqrt(n_ic))
        fig.add_trace(go.Scatter(x=x_ic, y=y_ic, 
                               fill='tozeroy', 
                               name=f'Intervalo de Confianza {nivel_conf:.0%}',
                               line=dict(color='green', width=0),
                               fillcolor='rgba(0, 255, 0, 0.3)',
                               showlegend=True))
        
        # Agregar líneas verticales para los puntos críticos
        for punto in [ic_lower, ic_upper]:
            fig.add_vline(x=punto, 
                         line_dash="dash", 
                         line_color="red",
                         annotation_text=f"{punto:.2f}",
                         annotation_position="top")
        
        # Agregar línea vertical para la media
        fig.add_vline(x=media_muestral,
                     line_color="green",
                     annotation_text=f"Media: {media_muestral:.2f}",
                     annotation_position="top")
        
        # Personalizar el diseño
        fig.update_layout(
            title=f'Intervalo de Confianza para la Media de {var_ic_media_t} ({nivel_conf:.0%})',
            xaxis_title=var_ic_media_t,
            yaxis_title='Densidad',
            showlegend=True,
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            annotations=[
                dict(x=media_muestral, y=max(y)*1.1,
                     text=f"IC: [{ic_lower:.2f}, {ic_upper:.2f}]",
                     showarrow=False)
            ]
        )
        
        st.plotly_chart(fig)
        
        # Interpretación
        st.write("### Interpretación:")
        
        if abs(t_value) > abs(stats.t.ppf(0.975, grados_libertad)):
            interpretacion = f"""
            El valor del estadístico t ({t_value:.4f}) cae en la región crítica 
            (|t| > {abs(stats.t.ppf(0.975, grados_libertad)):.4f}), lo que sugiere que hay evidencia estadística 
            significativa de que la media poblacional es diferente del valor de referencia 
            con un nivel de significancia de 0.05.
            
            La diferencia observada ({media_muestral:.4f}) es estadísticamente significativa.
            """
        else:
            interpretacion = f"""
            El valor del estadístico t ({t_value:.4f}) no cae en la región crítica 
            (|t| ≤ {abs(stats.t.ppf(0.975, grados_libertad)):.4f}), lo que sugiere que no hay evidencia estadística 
            significativa de que la media poblacional sea diferente del valor de referencia 
            con un nivel de significancia de 0.05.
            
            La diferencia observada ({media_muestral:.4f}) no es estadísticamente significativa.
            """
        
        st.write(interpretacion)

    # c) Intervalo para la diferencia de medias con varianza conocida
    with conf_tabs[2]:
        st.write("## 7.3 Intervalo de Confianza para la Diferencia de Medias (Varianza Conocida)")
        
        # Inputs para el usuario
        col1, col2 = st.columns(2)
        
        with col1:
            # Selección de variable numérica
            var_ic_diff = st.selectbox(
                "Seleccione la variable numérica",
                options=["Edad", "Frecuencia_Visitas", "Satisfaccion", "Preferencia"],
                key="var_ic_diff"
            )
            
            # Selección de variable para grupos
            var_grupo = st.selectbox(
                "Seleccione la variable para grupos",
                options=["Genero", "Importancia_Costo"],
                key="var_grupo_ic_diff"
            )
        
        with col2:
            # Inputs para las varianzas poblacionales
            sigma1 = st.number_input(
                f"Desviación estándar poblacional de {var_grupo} 1 (σ₁)",
                min_value=0.1,
                value=df[df[var_grupo] == df[var_grupo].unique()[0]][var_ic_diff].std(),
                step=0.1,
                key="sigma1_ic_diff"
            )
            
            sigma2 = st.number_input(
                f"Desviación estándar poblacional de {var_grupo} 2 (σ₂)",
                min_value=0.1,
                value=df[df[var_grupo] == df[var_grupo].unique()[1]][var_ic_diff].std(),
                step=0.1,
                key="sigma2_ic_diff"
            )
            
            # Nivel de confianza
            nivel_conf = st.slider(
                "Nivel de confianza",
                min_value=0.80,
                max_value=0.99,
                value=0.95,
                step=0.01,
                key="nivel_conf_ic_diff_dist"
            )
    
        # Cálculos para cada grupo
        datos1 = df[df[var_grupo] == df[var_grupo].unique()[0]][var_ic_diff]
        datos2 = df[df[var_grupo] == df[var_grupo].unique()[1]][var_ic_diff]
        
        n1 = len(datos1)
        n2 = len(datos2)
        media1 = datos1.mean()
        media2 = datos2.mean()
        diff_medias = media1 - media2
        
        # Cálculos del intervalo
        alpha = 1 - nivel_conf
        z_value = stats.norm.ppf(1 - alpha/2)
        error_est = z_value * np.sqrt((sigma1**2/n1) + (sigma2**2/n2))
        
        ic_lower = diff_medias - error_est
        ic_upper = diff_medias + error_est
        
        # Mostrar información del problema
        st.write("### Información del Problema")
        st.write(f"""
        **Grupo 1 ({var_grupo} 1):**
        - Tamaño de muestra (n₁): {n1}
        - Media muestral (x̄₁): {media1:.2f}
        - Desviación estándar poblacional (σ₁): {sigma1:.2f}
        
        **Grupo 2 ({var_grupo} 2):**
        - Tamaño de muestra (n₂): {n2}
        - Media muestral (x̄₂): {media2:.2f}
        - Desviación estándar poblacional (σ₂): {sigma2:.2f}
        
        **Diferencia de medias:**
        - x̄₁ - x̄₂ = {diff_medias:.2f}
        - Nivel de confianza: {nivel_conf:.0%}
        """)
        
        # Generar contexto automático
        contexto = f"""Se compara la variable '{var_ic_diff}' entre {var_grupo} 1 y {var_grupo} 2. 
        Con desviaciones estándar poblacionales conocidas de {sigma1:.2f} y {sigma2:.2f} respectivamente,
        se toman muestras de {n1} y {n2} observaciones. Las medias muestrales son {media1:.2f} para {var_grupo} 1 
        y {media2:.2f} para {var_grupo} 2. Se busca construir un intervalo de confianza al {nivel_conf:.0%} 
        para la diferencia de medias poblacionales."""
        st.write(contexto)
        
        # Fórmula
        st.write("### Fórmula:")
        latex_copyable(r"IC(\mu_1 - \mu_2) = (\bar{X}_1 - \bar{X}_2) \pm Z_{1-\frac{\alpha}{2}} \sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}", "ic_diff_formula")
        
        # Resolución de la fórmula
        st.write("### Resolución de la Fórmula:")
        latex_copyable(f"IC = ({media1:.4f} - {media2:.4f}) \pm {z_value:.4f} \sqrt{{{sigma1:.4f}²/{n1} + {sigma2:.4f}²/{n2}}}", "ic_diff_med_paso1")
        latex_copyable(f"IC = {diff_medias:.4f} \pm {z_value:.4f} \\times {np.sqrt(sigma1**2/n1 + sigma2**2/n2):.4f}", "ic_diff_med_paso2")
        latex_copyable(f"IC = {diff_medias:.4f} \pm {error_est:.4f}", "ic_diff_med_paso3")
        latex_copyable(f"IC = [{ic_lower:.4f}, {ic_upper:.4f}]", "ic_diff_med_paso4")

        # Cálculos intermedios
        st.write("### Cálculos:")
        st.write(f"""
        1. Valor crítico Z:
        - α = {alpha:.3f}
        - Z₍₁₋α/₂₎ = {z_value:.4f}
        
        2. Error estándar:
        - SE = {z_value:.4f} × √({sigma1:.2f}²/{n1} + {sigma2:.2f}²/{n2})
        - SE = {error_est:.4f}
        """)
        
        # Resultado del intervalo
        st.write("### Intervalo de Confianza:")
        st.write(f"IC = {diff_medias:.2f} ± {error_est:.2f}")
        st.write(f"IC = [{ic_lower:.2f}, {ic_upper:.2f}]")
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución normal
        x = np.linspace(diff_medias - 4*error_est, 
                       diff_medias + 4*error_est, 1000)
        y = stats.norm.pdf(x, diff_medias, error_est/z_value)
        
        # Crear el gráfico con plotly
        fig = go.Figure()
        
        # Agregar la curva normal
        fig.add_trace(go.Scatter(x=x, y=y, 
                               name='Distribución Normal',
                               line=dict(color='blue', width=2),
                               showlegend=True))
        
        # Agregar el área del intervalo de confianza
        x_ic = np.linspace(ic_lower, ic_upper, 1000)
        y_ic = stats.norm.pdf(x_ic, diff_medias, error_est/z_value)
        fig.add_trace(go.Scatter(x=x_ic, y=y_ic, 
                               fill='tozeroy', 
                               name=f'Intervalo de Confianza {nivel_conf:.0%}',
                               line=dict(color='green', width=0),
                               fillcolor='rgba(0, 255, 0, 0.3)',
                               showlegend=True))
        
        # Agregar líneas verticales para los puntos críticos
        for punto in [ic_lower, ic_upper]:
            fig.add_vline(x=punto, 
                         line_dash="dash", 
                         line_color="red",
                         annotation_text=f"{punto:.2f}",
                         annotation_position="top")
        
        # Agregar línea vertical para la diferencia de medias
        fig.add_vline(x=diff_medias,
                     line_color="green",
                     annotation_text=f"Diferencia: {diff_medias:.2f}",
                     annotation_position="top")
        
        # Personalizar el diseño
        fig.update_layout(
            title=f'Intervalo de Confianza para la Diferencia de Medias ({nivel_conf:.0%})',
            xaxis_title=f'Diferencia en {var_ic_diff} ({var_grupo} 1 - {var_grupo} 2)',
            yaxis_title='Densidad',
            showlegend=True,
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            annotations=[
                dict(x=diff_medias, y=max(y)*1.1,
                     text=f"IC: [{ic_lower:.2f}, {ic_upper:.2f}]",
                     showarrow=False)
            ]
        )
        
        st.plotly_chart(fig)
        
        # Interpretación
        st.write("### Interpretación")
        if ic_lower < 0 and ic_upper > 0:
            interpretacion = f"""
            Con un nivel de confianza del {nivel_conf:.0%}, la diferencia en {var_ic_diff} 
            entre {var_grupo} 1 y {var_grupo} 2 se encuentra entre {ic_lower:.2f} y {ic_upper:.2f}. Como el intervalo 
            contiene el cero, no hay evidencia suficiente para afirmar que existe una diferencia significativa 
            entre los grupos."""
        else:
            interpretacion = f"""
            Con un nivel de confianza del {nivel_conf:.0%}, la diferencia en {var_ic_diff} 
            entre {var_grupo} 1 y {var_grupo} 2 se encuentra entre {ic_lower:.2f} y {ic_upper:.2f}. Como el intervalo 
            no contiene el cero, hay evidencia de una diferencia significativa entre los grupos."""
        
        st.write(interpretacion)

    # f) Proporción
    with conf_tabs[3]:
        st.write("## 7.4 Intervalo de Confianza para la Proporción")
        
        st.write("""
        En esta sección analizaremos la proporción de visitantes satisfechos (calificación ≥4) 
        en toda la muestra.
        """)
        
        # Calcular datos reales de satisfacción
        satisfaccion_alta = 4  # Umbral de satisfacción alta
        n_total = len(df)
        n_satisfechos = sum(df['Satisfaccion'] >= satisfaccion_alta)
        p_hat = n_satisfechos/n_total
        q_hat = 1 - p_hat
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Mostrar datos calculados
            st.write("### Datos de la Muestra")
            st.write(f"""
            - Total de visitantes (n): {n_total}
            - Visitantes satisfechos (x): {n_satisfechos}
            - Proporción muestral (p̂): {p_hat:.4f}
            - Complemento (q̂): {q_hat:.4f}
            """)
            
            # Proporción hipotética
            p0 = st.number_input(
                "Proporción hipotética (π₀)",
                min_value=0.0,
                max_value=1.0,
                value=0.75,
                step=0.01,
                format="%.2f",
                key="p0_prop_ic"
            )
            
        with col2:
            # Nivel de confianza
            nivel_conf = st.slider(
                "Nivel de confianza",
                min_value=0.80,
                max_value=0.99,
                value=0.95,
                step=0.01,
                key="nivel_conf_prop_ic"
            )
            
            # Calcular tamaño del efecto (h de Cohen)
            h = 2 * np.arcsin(np.sqrt(p_hat)) - 2 * np.arcsin(np.sqrt(p0))
            
            # Determinar la magnitud del efecto
            if abs(h) < 0.2:
                efecto = "pequeño"
            elif abs(h) < 0.5:
                efecto = "mediano"
            else:
                efecto = "grande"
                
            st.write("### Tamaño del Efecto")
            st.write(f"""
            - h de Cohen: {h:.3f}
            - Interpretación: Efecto {efecto}
            """)
    
        # Cálculos del intervalo
        alpha = 1 - nivel_conf
        z_value = stats.norm.ppf(1 - alpha/2)
        error_est = z_value * np.sqrt((p_hat * q_hat)/n_total)
        
        ic_lower = max(0, p_hat - error_est)  # No permitir valores negativos
        ic_upper = min(1, p_hat + error_est)  # No permitir valores mayores a 1
        
        # Mostrar información del problema
        st.write("### Información del Problema")
        st.write(f"""
        Se analiza una muestra de {n_total} visitantes donde se encontraron {n_satisfechos} satisfechos 
        (calificación ≥ {satisfaccion_alta}).
        
        Queremos determinar si la proporción real de satisfacción es diferente de {p0:.0%}.
        
        - Proporción muestral (p̂): {p_hat:.4f}
        - Nivel de confianza: {nivel_conf:.0%}
        """)
        
        # Fórmula
        st.write("### Fórmula:")
        latex_copyable(r"IC(\pi) = \hat{p} \pm Z_{1-\frac{\alpha}{2}} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}", "ic_prop_formula")
        
        # Resolución de la fórmula
        st.write("### Resolución de la Fórmula:")
        latex_copyable(f"IC = {p_hat:.4f} \pm {z_value:.4f} \sqrt{{\\frac{{{p_hat:.4f}(1-{p_hat:.4f})}}{{{n_total}}}}}", "ic_prop_paso1")
        latex_copyable(f"IC = {p_hat:.4f} \pm {z_value:.4f} \\times {np.sqrt(p_hat*(1-p_hat)/n_total):.4f}", "ic_prop_paso2")
        latex_copyable(f"IC = {p_hat:.4f} \pm {error_est:.4f}", "ic_prop_paso3")
        latex_copyable(f"IC = [{ic_lower:.4f}, {ic_upper:.4f}]", "ic_prop_paso4")

        # Cálculos intermedios
        st.write("### Cálculos:")
        st.write(f"""
        1. Valor crítico Z:
        - α = {alpha:.3f}
        - Z₍₁₋α/₂₎ = {z_value:.4f}
        
        2. Error estándar:
        - SE = {z_value:.4f} × √({p_hat:.4f} × {q_hat:.4f}/{n_total})
        - SE = {error_est:.4f}
        
        3. Cálculo del intervalo:
        {p_hat:.4f} - {error_est:.4f} < π < {p_hat:.4f} + {error_est:.4f}
        {ic_lower:.4f} < π < {ic_upper:.4f}
        """)
        
        # Interpretación
        st.write("### Interpretación:")
        if p0 >= ic_lower and p0 <= ic_upper:
            interpretacion = f"""
            Con un {nivel_conf:.0%} de confianza, la proporción verdadera de visitantes satisfechos 
            se encuentra entre {ic_lower:.4f} y {ic_upper:.4f} ({ic_lower:.1%} y {ic_upper:.1%}).
            
            Como el valor hipotético ({p0:.4f}) está dentro del intervalo de confianza, 
            no hay evidencia suficiente para concluir que la proporción real sea diferente de {p0:.0%}.
            
            El tamaño del efecto (h de Cohen) es {h:.3f}, lo que se considera un efecto {efecto}.
            """
        else:
            interpretacion = f"""
            Con un {nivel_conf:.0%} de confianza, la proporción verdadera de visitantes satisfechos 
            se encuentra entre {ic_lower:.4f} y {ic_upper:.4f} ({ic_lower:.1%} y {ic_upper:.1%}).
            
            Como el valor hipotético ({p0:.4f}) está fuera del intervalo de confianza, 
            hay evidencia suficiente para concluir que la proporción real es diferente de {p0:.0%}.
            
            El tamaño del efecto (h de Cohen) es {h:.3f}, lo que se considera un efecto {efecto}.
            """
        st.write(interpretacion)
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución normal
        x_vals = np.linspace(max(0, p_hat - 4*error_est), 
                           min(1, p_hat + 4*error_est), 1000)
        y = stats.norm.pdf(x_vals, p_hat, error_est/z_value)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva normal
        fig.add_trace(go.Scatter(x=x_vals, y=y, mode='lines', name='Distribución Normal',
                               line=dict(color='blue')))
        
        # Agregar área del intervalo de confianza
        x_ic = np.linspace(ic_lower, ic_upper, 1000)
        y_ic = stats.norm.pdf(x_ic, p_hat, error_est/z_value)
        fig.add_trace(go.Scatter(x=x_ic, y=y_ic, 
                               fill='tozeroy', 
                               name=f'Intervalo de Confianza {nivel_conf:.0%}',
                               line=dict(color='green', width=0),
                               fillcolor='rgba(0, 255, 0, 0.3)'))
        
        # Agregar líneas verticales para los límites del intervalo
        for punto, texto in [(ic_lower, f"Límite inferior: {ic_lower:.4f}"), 
                           (ic_upper, f"Límite superior: {ic_upper:.4f}"),
                           (p_hat, f"Proporción muestral: {p_hat:.4f}"),
                           (p0, f"Proporción hipotética: {p0:.4f}")]:
            fig.add_vline(x=punto, 
                         line_dash="dash", 
                         line_color="red" if punto in [ic_lower, ic_upper] else "green" if punto == p_hat else "blue",
                         annotation_text=texto,
                         annotation_position="top")
        
        # Actualizar layout
        fig.update_layout(
            title=f'Intervalo de Confianza para la Proporción ({nivel_conf:.0%})',
            xaxis_title='Proporción',
            yaxis_title='Densidad',
            showlegend=True,
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            annotations=[
                dict(x=p_hat, y=max(y)*1.1,
                     text=f"IC: [{ic_lower:.2f}, {ic_upper:.2f}]",
                     showarrow=False)
            ]
        )
        
        st.plotly_chart(fig)
        
    # g) Diferencia de Proporciones
    with conf_tabs[4]:
        st.write("## 7.5 Intervalo de Confianza para la Diferencia de Proporciones")
        
        st.write("""
        En esta sección analizaremos la diferencia de proporciones de satisfacción alta (calificación ≥4) 
        entre visitantes masculinos y femeninos.
        """)
        
        # Calcular proporciones y tamaños de muestra por género
        satisfaccion_alta = 4  # Definimos satisfacción alta como ≥4
        
        # Grupo 1: Masculino (Género = 1)
        grupo1 = df[df['Genero'] == 1]
        n1 = len(grupo1)
        satisfechos1 = sum(grupo1['Satisfaccion'] >= satisfaccion_alta)
        p1 = satisfechos1 / n1
        
        # Grupo 2: Femenino (Género = 2)
        grupo2 = df[df['Genero'] == 2]
        n2 = len(grupo2)
        satisfechos2 = sum(grupo2['Satisfaccion'] >= satisfaccion_alta)
        p2 = satisfechos2 / n2
            
        # Entrada de datos (mostrando los valores reales calculados)
        col1, col2 = st.columns(2)
        
        with col1:
            # Grupo 1
            st.write("### Grupo 1 (Masculino)")
            p1_input = st.number_input(
                "Proporción del grupo 1 (p₁):",
                min_value=0.0,
                max_value=1.0,
                value=float(p1),
                step=0.0001,
                format="%.4f",
                key="p1_ic_diff_prop_dist"
            )
            n1_input = st.number_input(
                "Tamaño de muestra del grupo 1 (n₁):",
                min_value=1,
                value=int(n1),
                step=1,
                key="n1_ic_diff_prop_dist"
            )
            
        with col2:
            # Grupo 2
            st.write("### Grupo 2 (Femenino)")
            p2_input = st.number_input(
                "Proporción del grupo 2 (p₂):",
                min_value=0.0,
                max_value=1.0,
                value=float(p2),
                step=0.0001,
                format="%.4f",
                key="p2_ic_diff_prop_dist"
            )
            n2_input = st.number_input(
                "Tamaño de muestra del grupo 2 (n₂):",
                min_value=1,
                value=int(n2),
                step=1,
                key="n2_ic_diff_prop_dist"
            )
        
        # Nivel de confianza
        nivel_conf = st.slider("Nivel de Confianza", 
                             min_value=0.80, max_value=0.99, 
                             value=0.95, step=0.01, key="conf_diff_prop_dist_2")
        
        # Cálculos
        alpha = 1 - nivel_conf
        z_critico = stats.norm.ppf(1 - alpha/2)
        
        # Complementos
        q1 = 1 - p1_input
        q2 = 1 - p2_input
        
        # Error estándar
        error_est = np.sqrt((p1_input*q1)/n1_input + (p2_input*q2)/n2_input)
        
        # Límites del intervalo
        margen_error = z_critico * error_est
        ic_lower = p1_input - p2_input - margen_error
        ic_upper = p1_input - p2_input + margen_error
        
        # Mostrar resultados
        st.write("### Resultados")
        
        st.write(f"""
        #### Datos del grupo 1:
        - Proporción muestral (p₁) = {p1_input:.4f}
        - Complemento (q₁) = {q1:.4f}
        - Tamaño de muestra (n₁) = {n1_input}
        
        #### Datos del grupo 2:
        - Proporción muestral (p₂) = {p2_input:.4f}
        - Complemento (q₂) = {q2:.4f}
        - Tamaño de muestra (n₂) = {n2_input}
        
        #### Diferencia de proporciones:
        - p₁ - p₂ = {p1_input-p2_input:.4f}
        """)
        
        # Fórmula
        st.write("### Fórmula del Intervalo de Confianza")
        formula = r"p_1 - p_2 \pm Z_{1-\frac{\alpha}{2}} \sqrt{\frac{p_1q_1}{n_1} + \frac{p_2q_2}{n_2}}"
        latex_copyable(formula, "ic_diff_prop_formula")
        
        st.write("### Cálculos")
        latex_copyable(f"Z_{{1-\\frac{{\\alpha}}{{2}}}} = {z_critico:.4f}", "ic_diff_prop_paso1")
        latex_copyable(f"\\text{{Error estándar}} = \\sqrt{{\\frac{{{p1_input:.4f}\\times{q1:.4f}}}{{{n1_input}}} + \\frac{{{p2_input:.4f}\\times{q2:.4f}}}{{{n2_input}}}}} = {error_est:.4f}", "ic_diff_prop_paso2")
        latex_copyable(f"\\text{{Margen de error}} = {z_critico:.4f} \\times {error_est:.4f} = {margen_error:.4f}", "ic_diff_prop_paso3")
        
        # Intervalo de confianza
        st.write("### Intervalo de Confianza")
        st.write(f"""
        Con un nivel de confianza del {nivel_conf:.0%}, el intervalo de confianza para la diferencia de proporciones es:
        """)
        
        latex_copyable(f"{ic_lower:.4f} < π₁ - π₂ < {ic_upper:.4f}", "ic_diff_prop_result")
        
        # Interpretación
        st.write("### Interpretación:")
        
        # Calcular el tamaño del efecto (h de Cohen)
        h = 2 * np.arcsin(np.sqrt(p1_input)) - 2 * np.arcsin(np.sqrt(p2_input))
        
        # Determinar la magnitud del efecto
        if abs(h) < 0.2:
            efecto = "pequeño"
        elif abs(h) < 0.5:
            efecto = "mediano"
        else:
            efecto = "grande"
            
        # Definir umbral de significancia práctica (10% de diferencia)
        umbral_practico = 0.10
        
        if abs(ic_lower) < 0.01 and abs(ic_upper) > 0.01:
            interpretacion = f"""
            Con un {nivel_conf:.0%} de confianza, la diferencia en proporciones verdaderas entre los dos grupos 
            se encuentra entre {ic_lower:.4f} y {ic_upper:.4f} ({ic_lower:.1%} y {ic_upper:.1%}).
            
            Como el intervalo contiene el cero, no hay evidencia suficiente para concluir que existe 
            una diferencia estadísticamente significativa entre las proporciones de los dos grupos.
            
            El tamaño del efecto (h de Cohen) es {h:.3f}, lo que se considera un efecto {efecto}.
            """
        else:
            diferencia_significativa = any(abs(x) >= umbral_practico for x in [ic_lower, ic_upper])
            interpretacion = f"""
            Con un {nivel_conf:.0%} de confianza, la diferencia en proporciones verdaderas entre los dos grupos 
            se encuentra entre {ic_lower:.4f} y {ic_upper:.4f} ({ic_lower:.1%} y {ic_upper:.1%}).
            
            Como el intervalo no contiene el cero, hay evidencia suficiente para concluir que existe 
            una diferencia estadísticamente significativa entre las proporciones de los dos grupos.
            
            El tamaño del efecto (h de Cohen) es {h:.3f}, lo que se considera un efecto {efecto}.
            
            {"La diferencia también es prácticamente significativa, superando el umbral del 10%." if diferencia_significativa else
             "Sin embargo, la diferencia podría no ser prácticamente significativa, ya que no supera el umbral del 10%."}
            """
        st.write(interpretacion)
        
        # Visualización
        st.write("### Visualización")
        
        # Crear datos para la distribución normal
        x = np.linspace(p1_input - p2_input - 4*error_est, p1_input - p2_input + 4*error_est, 1000)
        y = stats.norm.pdf(x, p1_input - p2_input, error_est)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar la curva normal
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Normal',
                               line=dict(color='blue')))
        
        # Agregar área del intervalo de confianza
        x_ic = x[(x >= ic_lower) & (x <= ic_upper)]
        y_ic = y[(x >= ic_lower) & (x <= ic_upper)]
        
        fig.add_trace(go.Scatter(x=x_ic, y=y_ic, 
                               fill='tozeroy', 
                               name=f'Intervalo de Confianza {nivel_conf:.0%}',
                               line=dict(color='green', width=0),
                               fillcolor='rgba(0, 255, 0, 0.3)'))
        
        # Agregar líneas verticales para los límites del intervalo
        for punto, texto in [(ic_lower, f"Límite inferior: {ic_lower:.4f}"), 
                           (ic_upper, f"Límite superior: {ic_upper:.4f}"),
                           (p1_input - p2_input, f"Diferencia observada: {p1_input - p2_input:.4f}")]:
            fig.add_vline(x=punto, 
                         line_dash="dash", 
                         line_color="red",
                         annotation_text=texto,
                         annotation_position="top")
        
        # Agregar líneas para umbrales de significancia práctica
        fig.add_vline(x=umbral_practico, 
                     line_dash="dot",
                     line_color="gray",
                     annotation_text="Umbral de significancia práctica (10%)",
                     annotation_position="bottom")
        fig.add_vline(x=-umbral_practico, 
                     line_dash="dot",
                     line_color="gray")
        
        # Actualizar layout
        fig.update_layout(
            title=f"Intervalo de Confianza {nivel_conf:.0%} para la Diferencia de Proporciones",
            xaxis_title="Diferencia de Proporciones",
            yaxis_title="Densidad",
            showlegend=True
        )
        
        st.plotly_chart(fig)
        
    # h) Varianza
    with conf_tabs[5]:
        st.write("## 7.6 Intervalo de Confianza para la Varianza")
        
        st.write("""
        El intervalo de confianza para la varianza poblacional (σ²) nos permite estimar un rango de valores 
        donde se encuentra la verdadera varianza de la población, basándonos en la varianza muestral (s²).
        
        Este intervalo es útil cuando necesitamos:
        - Evaluar la dispersión de los datos en la población
        - Comparar la variabilidad entre diferentes poblaciones
        - Realizar control de calidad en procesos
        """)
        
        # Fórmula principal
        st.write("### Fórmula:")
        latex_copyable(r"IC(\sigma^2) = \left(\frac{(n-1)s^2}{\chi^2_{n-1,1-\frac{\alpha}{2}}}, \frac{(n-1)s^2}{\chi^2_{n-1,\frac{\alpha}{2}}}\right)", "ic_var_formula")
        
        st.write("""
        Donde:
        - s² = Varianza muestral
        - n = Tamaño de la muestra
        - χ² = Valor crítico de la distribución chi-cuadrado
        - α = Nivel de significancia (1 - nivel de confianza)
        """)
        
        # Pasos de cálculo
        st.write("### Pasos de cálculo:")
        latex_copyable(r"\text{Límite inferior: } \frac{(n-1)s^2}{\chi^2_{n-1,1-\frac{\alpha}{2}}}", "ic_var_paso1")
        latex_copyable(r"\text{Límite superior: } \frac{(n-1)s^2}{\chi^2_{n-1,\frac{\alpha}{2}}}", "ic_var_paso2")
