import pandas as pd
import numpy as np
from scipy import stats

# Leer datos
df = pd.read_csv('../data/encuesta_recreacion_numerica.csv')

# Calcular estadísticos para la edad
edad_media = df['Edad'].mean()
edad_std = df['Edad'].std()
n = len(df)

print(f"Estadísticos para Edad:")
print(f"Media: {edad_media:.2f}")
print(f"Desviación estándar: {edad_std:.2f}")
print(f"Tamaño de muestra: {n}")
