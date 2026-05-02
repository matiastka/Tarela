"""
Este ejemplo se comprenderá una vez que hayan visto el método de Newton-Raphson para la búsqueda de raíces de una ecuación no lineal.

Situación: datos: una función f(x), una "semilla" x0 y una tolerancia.

Algoritmo: 
1. calcular x1 = x0 - (f(x0) / f'(x0))
2. si |x1 - x0| <= TOLERANCIA, la salida es x1 y cota1.
3. si no, renombrar x0 = x1 y repetir desde (1)

Como no sabemos la cantidad de iteraciones, usamos un while
Ademas queremos 6 digitos significativos por lo que TOLERANCIA = 0.5 *10^-6 (hasta 6 digitos significativos). 
"""
TOLERANCIA = 0.5e-2
import numpy as np

def f(x): 
    """
    Pre: 
        x es un numero racional.
    Post: 
        Devuelve el valor de la funcion f(x) evaluada en x.
    """
    return 80 * np.exp(-2*x) + 20 * np.exp(-0.1*x) - 50


def df(x): 
    """
    Pre: 
        x es un numero racional
    Post: 
        Devuelve el valor de la funcion derivada f'(x) evaluada en x
    """
    return -160 * np.exp(-2*x) - 2 * np.exp(-0.1*x) 


def newton_raphson(cantidad_iteraciones, x0, multiplicidad_raiz):
    """
    Pre:
        cantidad_iteraciones es un numero entero:
            Si se desconocen la cantidad de iteraciones (cant<0)) se calcula hasta tolerancia = 0.5 *10^-6 \n
            Si se conoce la cantidad de iteraciones (cant>=0) calcula x_k (con k = cant_iteraciones)
        x0 es un numero racional y la semilla (valor definido por enunciado)\n
        multiplicidad_raiz es un numero entero que indica la multiplicidad de la raiz a analizar
    Post: 
        Imprime por pantalla el valor de α y la cota de error
    """
    if (cantidad_iteraciones < 0): # SI: Desconocemos la cantidad de iteraciones
        i = 0
        print("iteracion:", i)
        print("x0 =", x0)
        i = 1
        print("iteracion:", i)
        x1 = x0 - (multiplicidad_raiz * f(x0) / df(x0))
        print("x1 =", x1)
        cota1 = abs(x1-x0)
        print(f"Cota_{i} = {cota1}")

        while cota1 > TOLERANCIA: # Itera mientras la cota de error (de newton-raphson) sea mayor que la tolerancia
            i = i + 1
            print("iteracion:", i)
            x0 = x1
            x1 = x0 - (multiplicidad_raiz * f(x0) / df(x0))
            print(f"x{i} = {x1}")
            cota1 = abs(x1-x0)
            print(f"Cota_{i} = {cota1}")
        print(f"α = {x1}")
        print(f"Cota_error = {cota1}")

    else: # SI: Conocemos la cantidad de iteraciones
        print("iteracion: 0")
        print("x0 =", x0)

        for i in range(1, cantidad_iteraciones + 1):
            print("Iteracion:", i)
            x1 = x0 - (multiplicidad_raiz * f(x0) / df(x0))
            cota1 = abs(x1 - x0)
            x0 = x1
            print(f"x{i} = {x1}")
            print(f"Cota_error = {cota1}")
        print(f"α = {x1}")
        print(f"Cota_error = {cota1}")
        
newton_raphson(3, 0.5, 1)

# print(f"\n p = {np.log(3.586706348590596e-07/0.00060733998101975) / np.log(0.00060733998101975/0.02542751193857168)}\n")




