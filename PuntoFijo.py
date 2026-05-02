import numpy as np
def g(x):
    return x - abs(np.sin(1.35-x)) * 0.05 - 0.002

def punto_fijo(a, b, cota_error):
    k = 0
    print(f"\niteracion {k}")

    x_actual = a # en este caso la semilla es 1.6 (1er valor en el intervalo)

    print(f"x_{k} (semilla) = {x_actual}")
    x = g(x_actual)
    print(f"x_{k+1} = {x}")
    cota_error_actual = abs(x - x_actual)
    print(f"cota_error_{k} = {cota_error_actual}")
    # Si quiseramos calcular la cota error de error que va a tener nuestro calculo se hace como: (M/(1-M)) * abs(x-x_actual), siendo M el max(abs(g'(x))) para todo x en el intervalo
    # cota_error_actual_alternativa = (M/(1-M)) * abs(x-x_actual) 
    # print(f"cota_error_actual_alternativa = {cota_error_actual_alternativa}")
    while (cota_error_actual > cota_error):
        k = k + 1
        print(f"\niteracion {k}")
        x_actual = x
        print(f"x_{k} = {x_actual}")
        x = g(x)
        print(f"x_{k+1} = {x}")
        cota_error_actual = abs(x - x_actual)
        print(f"cota_error_{k} = {cota_error_actual}")
    
    print(f"\nx_{k} = {x}\ncota_error_{k} = {cota_error_actual}")

punto_fijo(1.2,1.3,0.001)
