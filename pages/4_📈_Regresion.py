import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import seaborn as sns

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
    page_title="Análisis de Regresión",
    page_icon="📈",
    layout="wide"
)

# Función para cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv('data/encuesta_recreacion_numerica.csv')

# Cargar datos
df = cargar_datos()

# Título principal
st.title("📈 Análisis de Regresión")
st.markdown("""
Este capítulo se centra en el análisis de regresión, una herramienta estadística fundamental 
para modelar y analizar las relaciones entre variables. Exploraremos dos tipos principales 
de regresión:
""")

# Crear tabs principales
main_tabs = st.tabs([
    "1.1 Regresión Lineal Simple",
    "1.2 Regresión Lineal Múltiple"
])

# 1.1 Regresión Lineal Simple
with main_tabs[0]:
    st.header("1.1 Regresión Lineal Simple")
    
    st.markdown("""
    La regresión lineal simple nos permite modelar la relación entre dos variables: 
    una variable independiente (X) y una variable dependiente (Y).
    """)
    
    # Selector de variables
    relacion = st.selectbox(
        "Seleccione la relación a analizar:",
        [
            "Satisfacción vs Edad",
            "Satisfacción vs Frecuencia de Visitas",
            "Preferencia vs Importancia del Costo"
        ]
    )
    
    # Definir variables según la selección
    if relacion == "Satisfacción vs Edad":
        x_var = 'Edad'
        y_var = 'Satisfaccion'
        x_label = 'Edad'
        y_label = 'Satisfacción'
    elif relacion == "Satisfacción vs Frecuencia de Visitas":
        x_var = 'Frecuencia_Visitas'
        y_var = 'Satisfaccion'
        x_label = 'Frecuencia de Visitas'
        y_label = 'Satisfacción'
    else:  # Preferencia vs Importancia del Costo
        x_var = 'Importancia_Costo'
        y_var = 'Preferencia'
        x_label = 'Importancia del Costo'
        y_label = 'Preferencia'
    
    st.markdown(f"""
    ### Ejemplo: Relación entre {y_label} y {x_label}
    
    Analizaremos si existe una relación lineal entre {x_label.lower()} y {y_label.lower()} 
    de los visitantes.
    """)
    
    # Preparar datos para la regresión
    X = df[x_var].values.reshape(-1, 1)
    y = df[y_var].values
    
    # Crear tabla de cálculos intermedios
    calculos_df = pd.DataFrame({
        'X': X.flatten(),
        'Y': y,
        'XY': X.flatten() * y,
        'X²': X.flatten() ** 2,
        'Y²': y ** 2
    })
    
    # Calcular sumatorias
    sumas = calculos_df.sum()
    medias = calculos_df.mean()
    n = len(calculos_df)
    
    # Calcular coeficientes manualmente
    beta1 = (n * sumas['XY'] - sumas['X'] * sumas['Y']) / (n * sumas['X²'] - sumas['X']**2)
    beta0 = (sumas['Y'] - beta1 * sumas['X']) / n
    
    # Mostrar tabla con cálculos
    st.markdown("### Tabla de Cálculos Intermedios")
    st.dataframe(calculos_df.style.format("{:.4f}"))
    
    # Mostrar sumatorias y medias
    st.markdown("### Sumatorias y Medias")
    st.dataframe(pd.DataFrame({
        'Suma': sumas,
        'Media': medias
    }).style.format("{:.4f}"))
    
    # Mostrar fórmulas y cálculos
    st.markdown("""
    ### Fórmulas y Cálculos
    
    Para la regresión lineal simple Y = β₀ + β₁X, calculamos:
    """)
    
    st.markdown("**β₁ (pendiente):**")
    # Fórmula general de beta1
    formula_beta1 = r"\beta_1 = \frac{n\sum XY - \sum X\sum Y}{n\sum X^2 - (\sum X)^2}"
    latex_copyable(formula_beta1, "beta1_general")
    
    # Fórmula con valores de beta1
    formula_beta1_val = r"\beta_1 = \frac{(%d)(%.4f) - (%.4f)(%.4f)}{(%d)(%.4f) - (%.4f)^2} = %.4f" % (
        n, sumas['XY'], sumas['X'], sumas['Y'],
        n, sumas['X²'], sumas['X'], beta1
    )
    latex_copyable(formula_beta1_val, "beta1_valores")
    
    st.markdown("**β₀ (intercepto):**")
    # Fórmula general de beta0
    formula_beta0 = r"\beta_0 = \frac{\sum Y - \beta_1\sum X}{n}"
    latex_copyable(formula_beta0, "beta0_general")
    
    # Fórmula con valores de beta0
    formula_beta0_val = r"\beta_0 = \frac{%.4f - (%.4f)(%.4f)}{%d} = %.4f" % (
        sumas['Y'], beta1, sumas['X'], n, beta0
    )
    latex_copyable(formula_beta0_val, "beta0_valores")
    
    st.markdown("Por lo tanto, la ecuación de regresión es:")
    
    # Mostrar la ecuación de regresión
    st.markdown("### Ecuación de Regresión")
    
    # Fórmula general
    formula_reg = r"Y = \beta_0 + \beta_1X"
    latex_copyable(formula_reg, "eq_reg_general")
    
    # Fórmula con valores
    formula_reg_val = r"Y = %.4f + %.4fX" % (beta0, beta1)
    latex_copyable(formula_reg_val, "eq_reg_valores")
    
    # Crear y ajustar el modelo
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Predicciones
    y_pred = modelo.predict(X)
    
    # Calcular R² y RMSE
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    # Calcular estadísticas adicionales usando scipy
    n = len(X)
    p = 1  # número de predictores
    
    # Error estándar de los coeficientes
    mse = mean_squared_error(y, y_pred)
    var_e = mse * (n-1) / (n-p-1)
    sd_b = np.sqrt(var_e / np.sum((X - X.mean())**2))
    
    # t-valor y p-valor para la pendiente
    t_stat = modelo.coef_[0] / sd_b
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-2))
    
    # Mostrar estadísticas del modelo
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Coeficiente de Determinación (R²)", f"{r2:.4f}")
    with col2:
        st.metric("Error Cuadrático Medio (RMSE)", f"{rmse:.4f}")
    with col3:
        st.metric("P-valor", f"{p_value:.4f}")
    
    # Mostrar la ecuación de regresión con el modelo ajustado
    st.markdown("### Ecuación de Regresión")
    
    # Fórmula con coeficientes del modelo
    formula_modelo = r"Y = %.4f + %.4fX" % (modelo.intercept_, modelo.coef_[0])
    latex_copyable(formula_modelo, "eq_modelo")
    
    st.markdown("""
    **Estadísticas de la pendiente:**
    - Error estándar: %.4f
    - t-valor: %.4f
    - p-valor: %.4f
    
    Donde:
    - Y: %s
    - X: %s
    """ % (sd_b, t_stat, p_value, y_label, x_label))
    
    # Visualización
    st.markdown("### Visualización")
    
    # Crear figura
    fig = go.Figure()
    
    # Agregar puntos de datos
    fig.add_trace(go.Scatter(
        x=X.flatten(),
        y=y,
        mode='markers',
        name='Datos observados',
        marker=dict(
            color='blue',
            size=8,
            line=dict(
                color='black',
                width=1
            )
        ),
        hovertemplate=
        f'{x_label}: %{{x}}<br>' +
        f'{y_label}: %{{y}}<br>' +
        '<extra></extra>'
    ))
    
    # Agregar línea de regresión
    X_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_line = modelo.predict(X_line)
    
    fig.add_trace(go.Scatter(
        x=X_line.flatten(),
        y=y_line,
        mode='lines',
        name='Línea de regresión',
        line=dict(color='red', width=2)
    ))
    
    # Actualizar layout
    fig.update_layout(
        title=f'Regresión Lineal: {y_label} vs {x_label}',
        xaxis_title=x_label,
        yaxis_title=y_label,
        showlegend=True,
        hovermode='closest'
    )
    
    st.plotly_chart(fig)
    
    # Análisis de residuos
    st.markdown("### Análisis de Residuos")
    
    # Calcular residuos
    residuos = y - y_pred
    
    # Crear figura para residuos
    fig_residuos = go.Figure()
    
    # Agregar puntos de residuos
    fig_residuos.add_trace(go.Scatter(
        x=y_pred,
        y=residuos,
        mode='markers',
        name='Residuos',
        marker=dict(color='blue')
    ))
    
    # Agregar línea horizontal en y=0
    fig_residuos.add_hline(
        y=0,
        line_dash="dash",
        line_color="red",
        annotation_text="y=0"
    )
    
    # Actualizar layout
    fig_residuos.update_layout(
        title='Gráfico de Residuos',
        xaxis_title='Valores Predichos',
        yaxis_title='Residuos',
        showlegend=True
    )
    
    st.plotly_chart(fig_residuos)
    
    # Interpretación
    st.markdown("""
    ### Interpretación de Resultados
    
    1. **Coeficiente de Determinación (R²):**
       - Indica qué proporción de la variabilidad en la satisfacción es explicada por la frecuencia de visitas
       - Un R² cercano a 1 indica un buen ajuste del modelo
    
    2. **Error Cuadrático Medio (RMSE):**
       - Mide la magnitud promedio de los errores de predicción
       - Un RMSE menor indica mejores predicciones
    
    3. **Significancia de la pendiente:**
       - El p-valor indica si la relación es estadísticamente significativa
       - Si p-valor < 0.05, la relación es significativa
    
    4. **Gráfico de Dispersión:**
       - Los puntos muestran los datos reales
       - La línea roja representa el modelo de regresión ajustado
    
    5. **Gráfico de Residuos:**
       - Ayuda a verificar los supuestos del modelo
       - Idealmente, los residuos deberían:
         * Distribuirse aleatoriamente alrededor de cero
         * No mostrar patrones evidentes
    """)

# 1.2 Regresión Lineal Múltiple
with main_tabs[1]:
    st.header("1.2 Regresión Lineal Múltiple")
    
    st.markdown("""
    La regresión lineal múltiple nos permite modelar la relación entre varias variables 
    independientes (X₁, X₂, ..., Xₙ) y una variable dependiente (Y).
    
    ### Ejemplo: Satisfacción explicada por Edad y Frecuencia de Visitas
    
    Analizaremos cómo la edad y la frecuencia de visitas influyen en conjunto sobre 
    el nivel de satisfacción de los visitantes.
    """)
    
    # Preparar datos para la regresión múltiple (primeros 10 registros)
    df_10 = df.head(10)
    X = df_10[['Edad', 'Frecuencia_Visitas']]
    y = df_10['Satisfaccion']
    
    # Crear tabla de cálculos intermedios
    calculos_df = pd.DataFrame({
        'Y': y,
        'X₁': X['Edad'],
        'X₂': X['Frecuencia_Visitas'],
        'Y*X₁': y * X['Edad'],
        'Y*X₂': y * X['Frecuencia_Visitas'],
        'X₁*X₂': X['Edad'] * X['Frecuencia_Visitas'],
        'X₁²': X['Edad']**2,
        'X₂²': X['Frecuencia_Visitas']**2
    })
    
    # Calcular sumatorias
    sumas = calculos_df.sum()
    
    # Variables para las fórmulas
    n = len(calculos_df)
    sum_y = sumas['Y']
    sum_x1 = sumas['X₁']
    sum_x2 = sumas['X₂']
    sum_yx1 = sumas['Y*X₁']
    sum_yx2 = sumas['Y*X₂']
    sum_x1x2 = sumas['X₁*X₂']
    sum_x1_2 = sumas['X₁²']
    sum_x2_2 = sumas['X₂²']
    
    # Mostrar tabla con cálculos
    st.markdown("### Tabla de Cálculos Intermedios (n=10)")
    st.dataframe(calculos_df.style.format("{:.4f}"))
    
    # Mostrar sumatorias
    st.markdown("### Sumatorias")
    st.dataframe(pd.DataFrame({
        'Suma': sumas
    }).style.format("{:.4f}"))
    
    # Ecuaciones normales
    st.markdown("### Ecuaciones Normales")
    st.markdown("Para encontrar los coeficientes β₀, β₁ y β₂, partimos de las ecuaciones normales:")
    
    # Primera ecuación
    formula1 = r"\sum Y = n\beta_0 + \beta_1\sum X_1 + \beta_2\sum X_2"
    latex_copyable(formula1, "eq_normal_1")
    
    # Segunda ecuación
    formula2 = r"\sum X_1Y = \beta_0\sum X_1 + \beta_1\sum X_1^2 + \beta_2\sum X_1X_2"
    latex_copyable(formula2, "eq_normal_2")
    
    # Tercera ecuación
    formula3 = r"\sum X_2Y = \beta_0\sum X_2 + \beta_1\sum X_1X_2 + \beta_2\sum X_2^2"
    latex_copyable(formula3, "eq_normal_3")
    
    st.markdown("Reemplazando los valores:")
    
    # Sistema de ecuaciones con valores
    formula4 = r"\begin{align*} %.4f &= %.4f\beta_0 + %.4f\beta_1 + %.4f\beta_2 \\ %.4f &= %.4f\beta_0 + %.4f\beta_1 + %.4f\beta_2 \\ %.4f &= %.4f\beta_0 + %.4f\beta_1 + %.4f\beta_2 \end{align*}" % (
        sum_y, n, sum_x1, sum_x2,
        sum_yx1, sum_x1, sum_x1_2, sum_x1x2,
        sum_yx2, sum_x2, sum_x1x2, sum_x2_2
    )
    latex_copyable(formula4, "eq_system")
    
    # Calcular determinantes para el método de Cramer
    A = np.array([
        [n, sum_x1, sum_x2],
        [sum_x1, sum_x1_2, sum_x1x2],
        [sum_x2, sum_x1x2, sum_x2_2]
    ])
    det_principal = np.linalg.det(A)
    
    # Matrices para cada β
    A0 = np.array([
        [sum_y, sum_x1, sum_x2],
        [sum_yx1, sum_x1_2, sum_x1x2],
        [sum_yx2, sum_x1x2, sum_x2_2]
    ])
    
    A1 = np.array([
        [n, sum_y, sum_x2],
        [sum_x1, sum_yx1, sum_x1x2],
        [sum_x2, sum_yx2, sum_x2_2]
    ])
    
    A2 = np.array([
        [n, sum_x1, sum_y],
        [sum_x1, sum_x1_2, sum_yx1],
        [sum_x2, sum_x1x2, sum_yx2]
    ])
    
    det_0 = np.linalg.det(A0)
    det_1 = np.linalg.det(A1)
    det_2 = np.linalg.det(A2)
    
    st.markdown("### Proceso de Cálculo de Coeficientes")
    st.markdown("Usando el método de Cramer, calculamos cada β:")
    
    # Fórmula general de Cramer
    formula_cramer = r"\beta_i = \frac{|A_i|}{|A|}"
    latex_copyable(formula_cramer, "cramer_general")
    
    st.markdown("Donde |A| es el determinante de la matriz principal:")
    
    # Matriz A principal
    matriz_A = r"\begin{vmatrix} %.4f & %.4f & %.4f \\ %.4f & %.4f & %.4f \\ %.4f & %.4f & %.4f \end{vmatrix} = %.4f" % (
        n, sum_x1, sum_x2,
        sum_x1, sum_x1_2, sum_x1x2,
        sum_x2, sum_x1x2, sum_x2_2,
        det_principal
    )
    latex_copyable(matriz_A, "matriz_A")
    
    # Para β₀
    st.markdown("Para β₀:")
    matriz_A0 = r"\begin{vmatrix} %.4f & %.4f & %.4f \\ %.4f & %.4f & %.4f \\ %.4f & %.4f & %.4f \end{vmatrix} = %.4f" % (
        sum_y, sum_x1, sum_x2,
        sum_yx1, sum_x1_2, sum_x1x2,
        sum_yx2, sum_x1x2, sum_x2_2,
        det_0
    )
    latex_copyable(matriz_A0, "matriz_A0")
    
    beta0_calc = r"\beta_0 = \frac{%.4f}{%.4f} = %.4f" % (det_0, det_principal, det_0/det_principal)
    latex_copyable(beta0_calc, "beta0_calc")
    
    # Para β₁
    st.markdown("Para β₁:")
    matriz_A1 = r"\begin{vmatrix} %.4f & %.4f & %.4f \\ %.4f & %.4f & %.4f \\ %.4f & %.4f & %.4f \end{vmatrix} = %.4f" % (
        n, sum_y, sum_x2,
        sum_x1, sum_yx1, sum_x1x2,
        sum_x2, sum_yx2, sum_x2_2,
        det_1
    )
    latex_copyable(matriz_A1, "matriz_A1")
    
    beta1_calc = r"\beta_1 = \frac{%.4f}{%.4f} = %.4f" % (det_1, det_principal, det_1/det_principal)
    latex_copyable(beta1_calc, "beta1_calc")
    
    # Para β₂
    st.markdown("Para β₂:")
    matriz_A2 = r"\begin{vmatrix} %.4f & %.4f & %.4f \\ %.4f & %.4f & %.4f \\ %.4f & %.4f & %.4f \end{vmatrix} = %.4f" % (
        n, sum_x1, sum_y,
        sum_x1, sum_x1_2, sum_yx1,
        sum_x2, sum_x1x2, sum_yx2,
        det_2
    )
    latex_copyable(matriz_A2, "matriz_A2")
    
    beta2_calc = r"\beta_2 = \frac{%.4f}{%.4f} = %.4f" % (det_2, det_principal, det_2/det_principal)
    latex_copyable(beta2_calc, "beta2_calc")
    
    # Resolver el sistema de ecuaciones
    coef = np.array([det_0/det_principal, det_1/det_principal, det_2/det_principal])
    
    # Mostrar ecuación final e interpretación
    st.markdown("### Ecuación de Regresión Múltiple")
    
    # Ecuación general
    eq_general = r"Y = \beta_0 + \beta_1X_1 + \beta_2X_2"
    latex_copyable(eq_general, "eq_multiple_general")
    
    # Ecuación con valores
    eq_valores = r"Y = %.4f + %.4f X_1 + %.4f X_2" % (coef[0], coef[1], coef[2])
    latex_copyable(eq_valores, "eq_multiple_valores")
    
    st.markdown("""
    Donde:
    - Y: Satisfacción
    - X₁: Edad
    - X₂: Frecuencia de Visitas
    """)
    
    # Crear y ajustar el modelo
    modelo_multiple = LinearRegression()
    modelo_multiple.fit(X, y)
    
    # Predicciones
    y_pred = modelo_multiple.predict(X)
    
    # Calcular R² y RMSE
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    # Calcular estadísticas adicionales
    n = len(X)
    p = 2  # número de predictores
    
    # Calcular error estándar de los coeficientes
    mse = mean_squared_error(y, y_pred)
    X_with_intercept = np.column_stack([np.ones(n), X])
    var_coef = mse * np.linalg.inv(X_with_intercept.T @ X_with_intercept).diagonal()
    se_coef = np.sqrt(var_coef)
    
    # Calcular t-valores y p-valores
    t_stats = np.r_[modelo_multiple.intercept_, modelo_multiple.coef_] / se_coef
    p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), df=n-p-1))
    
    # Mostrar estadísticas del modelo
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Coeficiente de Determinación (R²)", f"{r2:.4f}")
    with col2:
        st.metric("Error Cuadrático Medio (RMSE)", f"{rmse:.4f}")
    
    # Crear DataFrame con resultados
    coef_names = ['Intercepto', 'Edad', 'Frecuencia_Visitas']
    resultados = pd.DataFrame({
        'Coeficiente': np.r_[modelo_multiple.intercept_, modelo_multiple.coef_],
        'Error Estándar': se_coef,
        't-valor': t_stats,
        'p-valor': p_values
    }, index=coef_names)
    
    st.markdown("### Resultados del Modelo")
    st.dataframe(resultados.style.format({
        'Coeficiente': '{:.4f}',
        'Error Estándar': '{:.4f}',
        't-valor': '{:.4f}',
        'p-valor': '{:.4f}'
    }))
    
    # Ecuación de regresión
    st.markdown(f"""
    ### Ecuación de Regresión
    
    Y = {modelo_multiple.intercept_:.4f} + {modelo_multiple.coef_[0]:.4f}X₁ + {modelo_multiple.coef_[1]:.4f}X₂
    
    Donde:
    - Y: Satisfacción
    - X₁: Edad
    - X₂: Frecuencia de Visitas
    """)
    
    # Visualización 3D
    st.markdown("### Visualización 3D")
    
    # Crear malla para la superficie
    x1_range = np.linspace(X['Edad'].min(), X['Edad'].max(), 20)
    x2_range = np.linspace(X['Frecuencia_Visitas'].min(), X['Frecuencia_Visitas'].max(), 20)
    x1_mesh, x2_mesh = np.meshgrid(x1_range, x2_range)
    X_mesh = np.column_stack((x1_mesh.ravel(), x2_mesh.ravel()))
    y_mesh = modelo_multiple.predict(X_mesh).reshape(x1_mesh.shape)
    
    # Crear figura 3D
    fig = go.Figure()
    
    # Agregar puntos de datos
    fig.add_trace(go.Scatter3d(
        x=X['Edad'],
        y=X['Frecuencia_Visitas'],
        z=y,
        mode='markers',
        marker=dict(
            size=6,
            color='blue',
            opacity=0.7
        ),
        name='Datos observados',
        hovertemplate=
        'Edad: %{x}<br>' +
        'Frecuencia: %{y}<br>' +
        'Satisfacción: %{z}<br>' +
        '<extra></extra>'
    ))
    
    # Agregar superficie de regresión
    fig.add_trace(go.Surface(
        x=x1_range,
        y=x2_range,
        z=y_mesh,
        opacity=0.7,
        colorscale='Viridis',
        name='Superficie de regresión',
        showscale=False
    ))
    
    # Actualizar layout
    fig.update_layout(
        title='Regresión Múltiple: Satisfacción vs Edad y Frecuencia de Visitas',
        scene=dict(
            xaxis_title='Edad',
            yaxis_title='Frecuencia de Visitas',
            zaxis_title='Satisfacción'
        ),
        showlegend=True,
        width=800,
        height=800
    )
    
    st.plotly_chart(fig)
    
    # Interpretación
    st.markdown("""
    ### Interpretación del Modelo
    
    - El **R²** nos indica qué porcentaje de la variabilidad en la satisfacción es explicada por la edad y la frecuencia de visitas.
    - Los **coeficientes** muestran el cambio esperado en la satisfacción por cada unidad de cambio en la variable correspondiente, manteniendo las otras variables constantes.
    - Los **p-valores** indican la significancia estadística de cada variable. Valores menores a 0.05 sugieren que la variable es significativa.
    - El **RMSE** nos da una idea del error promedio en las predicciones del modelo.
    """)
