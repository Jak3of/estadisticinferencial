import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from src.visualizations import StatisticalVisualizer
from src.analysis import StatisticalAnalyzer

def main():
    # Crear datos de ejemplo
    np.random.seed(42)
    n_samples = 100
    
    data = pd.DataFrame({
        'edad': np.random.normal(35, 10, n_samples),
        'ingreso': np.random.normal(50000, 15000, n_samples),
        'gastos': np.random.normal(30000, 10000, n_samples),
        'satisfaccion': np.random.randint(1, 6, n_samples),
        'grupo': np.random.choice(['A', 'B'], n_samples)
    })
    
    # Crear instancias de nuestras clases
    visualizer = StatisticalVisualizer()
    analyzer = StatisticalAnalyzer()
    
    # 1. Análisis Descriptivo
    print("\nEstadísticas Descriptivas:")
    print(analyzer.descriptive_stats(data))
    
    # 2. Visualizaciones
    print("\nGenerando visualizaciones...")
    
    # Distribución de edad
    visualizer.plot_distribution(data, 'edad', "Distribución de Edades")
    
    # Boxplot de ingresos por grupo
    visualizer.plot_boxplot(data, x='grupo', y='ingreso', 
                          title="Ingresos por Grupo")
    
    # Regresión entre ingresos y gastos
    visualizer.plot_regression(data, x='ingreso', y='gastos', 
                             title="Relación Ingresos vs Gastos")
    
    # Matriz de correlación
    visualizer.plot_correlation_matrix(data.select_dtypes(include=[np.number]))
    
    # 3. Análisis Estadístico
    print("\nPrueba de Normalidad (edad):")
    print(analyzer.normality_test(data, 'edad'))
    
    print("\nPrueba t para ingresos entre grupos:")
    print(analyzer.t_test(data, 'ingreso', 'grupo'))
    
if __name__ == "__main__":
    main()
