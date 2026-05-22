import numpy as np
h = 0.4
print(f"h = {h}")

def t(n):
    return n * h

def f(u, t):
    return -u + (t ** 2) + 2 * t - 2

def euler_explicito(cantidad_iteraciones):
    u = 0 #u0
    
    for n in range(0, cantidad_iteraciones):
        print(f"\nIteracion {n} (n = {n})\n")
        print(f"u_{n} = {u}")
        print(f"t_{n} = n * h = {t(n)}")

        u_proximo = u + h * f(u, t(n))
        print(f"u_{n+1} = {u_proximo}")
        u = u_proximo # actualiza u0 = u1
        # print(f"f({n}, {t(n)}) = {f(n,t(n))}") # Imprime cuanto da f(u, t(n)), para saber si lo hace bien
euler_explicito(5)    