# Análisis Estadístico de Datos de Recreación

## 📊 Descripción del Proyecto
Una aplicación web interactiva desarrollada con Streamlit para realizar análisis estadístico avanzado de datos de recreación. La aplicación proporciona herramientas para análisis descriptivo, inferencial, pruebas de hipótesis y análisis de regresión, con un enfoque especial en la transparencia de los cálculos y la interpretación de resultados.

## 🌟 Características Principales

### 1. Análisis Descriptivo
- Visualización de distribuciones
- Estadísticas resumen
- Gráficos interactivos
- Análisis de tendencias centrales y dispersión

### 2. Análisis Inferencial
- Intervalos de confianza
- Estimación de parámetros
- Visualizaciones estadísticas
- Interpretación de resultados

### 3. Pruebas de Hipótesis
- Pruebas paramétricas y no paramétricas
- Test de Runs
- Test de Signos
- Visualización de resultados
- Interpretación detallada

### 4. Análisis de Regresión
#### Regresión Lineal Simple
- Selección interactiva de variables
- Cálculos paso a paso detallados
- Visualización de la línea de regresión
- Interpretación de coeficientes

#### Regresión Lineal Múltiple
- Método de Cramer para cálculo de coeficientes
- Ecuaciones normales con LaTeX
- Visualización 3D de la superficie de regresión
- Análisis detallado de coeficientes

## 🛠️ Tecnologías Utilizadas
- **Python**: Lenguaje principal de desarrollo
- **Streamlit**: Framework para la interfaz web
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Cálculos numéricos
- **SciPy**: Análisis estadístico
- **Plotly**: Visualizaciones interactivas
- **Scikit-learn**: Modelos de regresión

## 📈 Características Técnicas
1. **Cálculos Transparentes**
   - Mostración paso a paso de fórmulas
   - Tablas de cálculos intermedios
   - Validación cruzada de resultados

2. **Visualizaciones Interactivas**
   - Gráficos dinámicos
   - Personalización de parámetros
   - Tooltips informativos

3. **Interpretación Estadística**
   - Explicaciones detalladas
   - Contexto de resultados
   - Guías de interpretación

## 🚀 Instalación y Uso

1. **Clonar el repositorio**
```bash
git clone [URL_del_repositorio]
```

2. **Crear y activar entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
streamlit run Home.py
```

## 📊 Estructura del Proyecto
```
ff/
├── Home.py                 # Página principal
├── data/                   # Datos de ejemplo
├── pages/                  # Páginas de la aplicación
│   ├── 2_🔍_Analisis_Inferencial.py
│   ├── 3_📊_Pruebas_Hipotesis.py
│   ├── 4_📈_Regresion.py
│   └── 5_📋_Reportes.py
├── src/                    # Código fuente
└── requirements.txt        # Dependencias
```

## 🎯 Resultados y Conclusiones del Análisis

### Hallazgos Clave del Análisis de Datos

1. **Perfil Demográfico**
   - Rango de edad diverso (20-41 años)
   - Distribución equilibrada de género
   - Alta variabilidad en frecuencia de visitas (1-4.5 veces)

2. **Patrones de Satisfacción**
   - Alta correlación entre satisfacción y preferencia
   - Importancia del costo como factor significativo
   - Niveles de satisfacción generalmente altos (promedio 4/5)

3. **Análisis de Comportamiento**
   - Mayor frecuencia de visitas en grupos de edad específicos
   - Correlación positiva entre importancia del costo y satisfacción
   - Patrones distintivos por género en preferencias

### Conclusiones Estadísticas

1. **Regresión Lineal**
   - Relación significativa entre edad y frecuencia de visitas
   - El costo impacta directamente en la satisfacción
   - Modelo predictivo confiable (R² > 0.7)

2. **Pruebas de Hipótesis**
   - Diferencias significativas por género
   - Validación de patrones de comportamiento
   - Confirmación de tendencias demográficas

3. **Análisis Inferencial**
   - Intervalos de confianza robustos
   - Estimaciones precisas de parámetros poblacionales
   - Validación cruzada de resultados

### Implicaciones Prácticas

1. **Gestión de Servicios**
   - Optimización de precios basada en sensibilidad
   - Personalización de servicios por segmento
   - Mejora continua basada en retroalimentación

2. **Estrategias de Marketing**
   - Segmentación efectiva por edad y género
   - Enfoque en factores clave de satisfacción
   - Programas de fidelización basados en frecuencia

3. **Desarrollo Futuro**
   - Implementación de mejoras basadas en datos
   - Monitoreo continuo de satisfacción
   - Adaptación de servicios según tendencias

### Impacto y Aplicaciones

1. **Toma de Decisiones**
   - Base estadística sólida para decisiones operativas
   - Identificación de áreas de mejora
   - Optimización de recursos

2. **Valor Educativo**
   - Demostración práctica de métodos estadísticos
   - Casos de estudio reales
   - Validación de teorías estadísticas

3. **Beneficios Organizacionales**
   - Mejor comprensión del usuario
   - Optimización de servicios
   - Incremento en satisfacción del cliente

## 👥 Contribución
Las contribuciones son bienvenidas. Por favor, sigue estos pasos:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## 🙏 Agradecimientos
- A todos los contribuidores del proyecto
- A la comunidad de Streamlit
- A los usuarios por su retroalimentación

---
Desarrollado con ❤️ por Nelson Correa &copy; 2024
