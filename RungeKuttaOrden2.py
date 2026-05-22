import numpy as np
h = 0.4
print(f"h = {h}")

def t(n):
    return n * h

def f(u, t):
    return -u + (t ** 2) + 2 * t - 2

def runge_kutta_O2(cantidad_iteraciones): 
    u_actual = 0 #u0
    
    for n in range(0, cantidad_iteraciones):
        print(f"\nIteracion {n} (n = {n})\n")
        print(f"u_{n} = {u_actual}")
        print(f"t_{n} = n * h = {t(n)}")

        q1 = h * f(u_actual, t(n))
        print(f"q1 = {q1}")
        
        q2 = h * f(u_actual + q1, t(n) + (h))
        print(f"q2 = {q2}")

        u_proximo = u_actual + (1/2) * (q1 + q2)
        print(f"u_{n+1} = {u_proximo}")
        u_actual = u_proximo # actualiza u_actual
runge_kutta_O2(5)