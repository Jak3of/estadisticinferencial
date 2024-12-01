import pandas as pd
import numpy as np
from scipy import stats

class StatisticalAnalyzer:
    def __init__(self):
        pass
    
    def descriptive_stats(self, data, columns=None):
        """
        Calcular estadísticas descriptivas básicas
        """
        if columns is None:
            columns = data.select_dtypes(include=[np.number]).columns
        return data[columns].describe()
    
    def normality_test(self, data, column):
        """
        Realizar prueba de normalidad (Shapiro-Wilk)
        """
        statistic, p_value = stats.shapiro(data[column])
        return {
            'test': 'Shapiro-Wilk',
            'statistic': statistic,
            'p_value': p_value,
            'is_normal': p_value > 0.05
        }
    
    def correlation_analysis(self, data, method='pearson'):
        """
        Realizar análisis de correlación
        """
        numeric_data = data.select_dtypes(include=[np.number])
        return numeric_data.corr(method=method)
    
    def t_test(self, data, column, group_column):
        """
        Realizar prueba t de Student para dos grupos independientes
        """
        groups = data[column].groupby(data[group_column])
        group1, group2 = [group for _, group in groups]
        t_stat, p_value = stats.ttest_ind(group1, group2)
        return {
            'test': 't-test',
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    def anova(self, data, dependent_var, group_var):
        """
        Realizar análisis de varianza (ANOVA)
        """
        groups = data[dependent_var].groupby(data[group_var])
        f_stat, p_value = stats.f_oneway(*[group for _, group in groups])
        return {
            'test': 'ANOVA',
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
