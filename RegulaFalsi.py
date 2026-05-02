import numpy as np
def f(x): 
    """
    Pre: 
        x es un numero racional.
    Post: 
        Devuelve el valor de la funcion f(x) evaluada en x.
    """
    return (x**2 / 4 - np.sin(x))

def regula_falsi_por_error(a,b,cota_error_pedida):
    k = 0
    # print(f"\nIteracion {k}")
    # print(f"a = {a}")
    # print(f"b = {b}")
    # print(f"f({a}) = {f(a)}")
    # print(f"f({b}) = {f(b)}")
    m = a - (b - a) * (f(a) / (f(b) - f(a)))
    # print(f"m_{k+1} = {m}")
    # print(f"f({m}) = {f(m)}")
    cota_error_actual = np.inf # No se puede calcular la cota_error_actual pero necestiamos que arranque el metodo
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
        m_actual = m
        m = a - (b - a) * (f(a) / (f(b) - f(a)))
        # print(f"m_{k+1} = {m}")
        # print(f"f({m}) = {f(m)}")
        cota_error_actual = m - m_actual
        print(f"cota_error_{k+1} = {cota_error_actual}")

    print(f"\nm_{k+1} = {m}\ncota_error = {cota_error_actual}")
print("Regula Falsi por cota de error absoluta 0.02")
regula_falsi_por_error(1.6,2,0.02)