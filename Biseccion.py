import numpy as np
"""
Metodo Biseccion:
Ejemplo: f(x) = x^2 / 4 - sen(x)
Intervalo = [1.6, 2]

Regla:
Si f(a) tiene mismo signo que f(m_k+1) entonces se actualiza a

"""

def f(x): 
    """
    Pre: 
        x es un numero racional.
    Post: 
        Devuelve el valor de la funcion f(x) evaluada en x.
    """
    return (x**2 / 4 - np.sin(x))

def biseccion_por_n_pasos(a, b, n):
    """
    """
    for k in range(0, n+1):
        # print(f"k (iteracion) = {k}")
        punto_medio = (a + b) / 2
        # print(f"a_{k} = {a}")
        # print(f"b_{k} = {b}")
        # print(f"f(a_{k}) = {f(a)}")
        # print(f"f(b_{k}) = {f(b)}")
        # print(f"â = m_{k+1} = {punto_medio}")
        # print(f"f(m_{k+1}) = {f(punto_medio)}")
        
        if (k != 0): # En la semilla no se calcula error
            cota_error = abs((b-a)/2)
            # print(f"cota_error = {cota_error}\n")

        if (f(a) * f(punto_medio) < 0):
            b = punto_medio
        elif (f(a) * (f(punto_medio)) > 0):
            a = punto_medio
    print(f"m_{k+1} = {punto_medio}\ncota_error = {cota_error}")

print("Biseccion por 4 pasos")
biseccion_por_n_pasos(1.6, 2, 4)


def biseccion_por_error(a,b,cota_error_pedida):
    k = 0
    # print(f"\nIteracion {k}")
    # print(f"a = {a}")
    # print(f"b = {b}")
    # print(f"f({a}) = {f(a)}")
    # print(f"f({b}) = {f(b)}")
    m = (a + b) / 2
    # print(f"m_{k+1} = {m}")
    # print(f"f({m}) = {f(m)}")
    cota_error_actual = abs((b - a) / 2)
    # print(f"cota_error_{k+1} = {cota_error_actual}")

    while cota_error_actual > cota_error_pedida:
        if (f(a) * f(m)) < 0:
            b = m
        elif (f(a) * f(m) > 0):
            a = m
        k = k+1
        # print(f"\nIteracion {k}")
        # print(f"f({a}) = {f(a)}")
        # print(f"f({b}) = {f(b)}")
        m = (a + b) / 2
        # print(f"m_{k+1} = {m}")
        # print(f"f({m}) = {f(m)}")
        cota_error_actual = abs((b - a) / 2)
        # print(f"cota_error_{k+1} = {cota_error_actual}")

    print(f"\nm_{k+1} = {m}\ncota_error = {cota_error_actual}")
print("Biseccion por cota de error absoluta 0.02")
biseccion_por_error(1.6,2,0.02)