import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class StatisticalVisualizer:
    def __init__(self):
        # Configurar el estilo de Seaborn
        sns.set_theme(style="whitegrid")
        
    def plot_distribution(self, data, column, title="Distribución"):
        """
        Crear un gráfico de distribución con histograma y KDE
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(data=data, x=column, kde=True)
        plt.title(title)
        plt.show()
    
    def plot_boxplot(self, data, x, y=None, title="Diagrama de Caja"):
        """
        Crear un diagrama de caja
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=data, x=x, y=y)
        plt.title(title)
        plt.show()
    
    def plot_regression(self, data, x, y, title="Regresión"):
        """
        Crear un gráfico de regresión con intervalo de confianza
        """
        plt.figure(figsize=(10, 6))
        sns.regplot(data=data, x=x, y=y)
        plt.title(title)
        plt.show()
    
    def plot_correlation_matrix(self, data, title="Matriz de Correlación"):
        """
        Crear un mapa de calor de correlaciones
        """
        plt.figure(figsize=(10, 8))
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', center=0)
        plt.title(title)
        plt.show()
    
    def plot_categorical_analysis(self, data, x, y, title="Análisis Categórico"):
        """
        Crear un gráfico de barras con error bars
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(data=data, x=x, y=y, ci=95)
        plt.title(title)
        plt.show()
