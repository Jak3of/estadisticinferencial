import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.visualizations import StatisticalVisualizer
from src.analysis import StatisticalAnalyzer

def cargar_datos():
    """Cargar y preparar los datos de la encuesta"""
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_datos = os.path.join(ruta_base, 'data', 'encuesta_recreacion.csv')
    df = pd.read_csv(ruta_datos)
    return df

def analisis_demografico(df, visualizer):
    """Análisis demográfico básico"""
    print("\n=== Análisis Demográfico ===")
    
    # Distribución por edad
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Edad')
    plt.title('Distribución por Grupos de Edad')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Distribución por género
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x='Género')
    plt.title('Distribución por Género')
    plt.tight_layout()
    plt.show()

def analisis_satisfaccion(df, visualizer):
    """Análisis de satisfacción"""
    print("\n=== Análisis de Satisfacción ===")
    
    # Satisfacción general
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Satisfacción', order=['Poco satisfecho', 'Poco satisfecha', 'Satisfecho', 'Satisfecha', 'Muy satisfecho', 'Muy satisfecha'])
    plt.title('Niveles de Satisfacción')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Satisfacción por género
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Satisfacción', hue='Género')
    plt.title('Satisfacción por Género')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def analisis_actividades(df, visualizer):
    """Análisis de actividades y frecuencia"""
    print("\n=== Análisis de Actividades ===")
    
    # Distribución de actividades
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Actividades')
    plt.title('Distribución de Número de Actividades')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Frecuencia de visitas
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Frecuencia de Visitas')
    plt.title('Frecuencia de Visitas')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def analisis_temporal(df, visualizer):
    """Análisis temporal"""
    print("\n=== Análisis Temporal ===")
    
    # Época del año
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Época del Año de Visita Frecuente')
    plt.title('Época del Año de Visita')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    # Cargar datos
    df = cargar_datos()
    
    # Crear instancias de nuestras clases
    visualizer = StatisticalVisualizer()
    analyzer = StatisticalAnalyzer()
    
    # Realizar análisis
    analisis_demografico(df, visualizer)
    analisis_satisfaccion(df, visualizer)
    analisis_actividades(df, visualizer)
    analisis_temporal(df, visualizer)
    
    # Estadísticas descriptivas básicas
    print("\n=== Resumen Estadístico ===")
    print(f"Total de encuestados: {len(df)}")
    print(f"\nDistribución por género:")
    print(df['Género'].value_counts())
    print(f"\nDistribución por edad:")
    print(df['Edad'].value_counts())
    print(f"\nNivel de satisfacción general:")
    print(df['Satisfacción'].value_counts())

if __name__ == "__main__":
    main()
