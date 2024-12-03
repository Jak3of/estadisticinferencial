# runs_test.py

import math

def runs_test(n1, n2, R):
    N = n1 + n2
    # Cálculo del número esperado de rachas (E[R])
    mean_R = (2 * n1 * n2) / N + 1
    # Cálculo de la varianza de las rachas (Var[R])
    var_R = (2 * n1 * n2 * (2 * n1 * n2 - N)) / (N**2 * (N - 1))
    # Cálculo del estadístico Z
    z = (R - mean_R) / math.sqrt(var_R)
    return mean_R, var_R, z

def main():
    print("Cálculo de z para la Prueba de Rachas")
    # Solicitar los valores al usuario
    n1 = int(input("Ingresa n₁ (número de signos positivos): "))
    n2 = int(input("Ingresa n₂ (número de signos negativos): "))
    R = int(input("Ingresa R (número de rachas observadas): "))

    mean_R, var_R, z = runs_test(n1, n2, R)
    print(f"\nResultados:")
    print(f"Número esperado de rachas (E[R]): {mean_R:.4f}")
    print(f"Varianza de las rachas (Var[R]): {var_R:.4f}")
    print(f"Valor calculado de z: {z:.4f}")

    # Interpretación del resultado
    alpha = 0.05  # Nivel de significancia
    z_critico = 1.96  # Valor crítico para una prueba bilateral al 5%
    print("\nInterpretación:")
    if abs(z) > z_critico:
        print(f"|z| = {abs(z):.4f} > {z_critico}, se rechaza la hipótesis nula (H₀).")
        print("Conclusión: Existe evidencia suficiente para afirmar que la secuencia NO es aleatoria.")
    else:
        print(f"|z| = {abs(z):.4f} ≤ {z_critico}, no se rechaza la hipótesis nula (H₀).")
        print("Conclusión: No existe evidencia suficiente para rechazar que la secuencia es aleatoria.")

if __name__ == "__main__":
    main()