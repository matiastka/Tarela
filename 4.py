import numpy as np
import matplotlib.pyplot as plt

# Usamos las mismas constantes y funciones (f, euler_explicito, runge_kutta_O2) de tu 1.py
from E1 import f, euler_explicito, runge_kutta_O2, x0, y0, vx0, vy0

h = 3600.0          # 1 hora paso de tiempo
dias = 180.0        # Simulación a largo plazo (~6 meses)
cantidad_iteraciones = int(dias * 24)

u0 = np.array([x0, y0, vx0, vy0])

# Ejecutar simulaciones a largo plazo
tray_euler_lp = euler_explicito(u0, h, cantidad_iteraciones)
tray_rk2_lp   = runge_kutta_O2(u0, h, cantidad_iteraciones)

# Calcular distancias en miles de km a lo largo del tiempo
dist_euler = np.sqrt(tray_euler_lp[:, 0]**2 + tray_euler_lp[:, 1]**2) / 1e3
dist_rk2   = np.sqrt(tray_rk2_lp[:, 0]**2 + tray_rk2_lp[:, 1]**2) / 1e3
tiempo_dias = np.arange(cantidad_iteraciones + 1) * h / 86400.0

# Graficar la evolución de la distancia
plt.figure(figsize=(12, 5))
plt.plot(tiempo_dias, dist_euler, 'r-', label='Euler Explícito', alpha=0.8)
plt.plot(tiempo_dias, dist_rk2, 'g-', label='Runge-Kutta O2', alpha=0.8)
plt.axhline(363300, color='gray', linestyle='--', label='Perigeo Esperado')
plt.axhline(405500, color='black', linestyle='--', label='Apogeo Esperado')
plt.xlabel('Tiempo (días)')
plt.ylabel('Distancia Tierra-Luna (km)')
plt.title('Punto 5: Comportamiento de la Órbita Lunar a Largo Plazo')
plt.legend()
plt.grid(True)
plt.show()