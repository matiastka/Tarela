import numpy as np
import matplotlib.pyplot as plt
# ── Constantes ──────────────────
G  = 6.674e-11
MT = 5.972e24         
# Perigeo de la Luna sobre el eje +x
x0  =  363300000      
y0  =  0.0            
vx0 =  0.0            
vy0 =  1_076.0        
# ── Métodos de Integración Numérica ──────────────────────────────────────────
def f(u, t):
    x, y, vx, vy = u
    dT = np.sqrt(x**2 + y**2)          # distancia Tierra-Luna
    alpha = np.arctan2(y, x)           # ángulo desde la Tierra
 
    # Fuerza de atracción gravitatoria terrestre
    ax = -G * MT / dT**2 * np.cos(alpha)
    ay = -G * MT / dT**2 * np.sin(alpha)
 
    return np.array([vx, vy, ax, ay])
def euler_explicito(u0, h, cantidad_iteraciones):
    u = u0.copy()
    trayectoria = [u.copy()]
    for n in range(cantidad_iteraciones):
        u = u + h * f(u, n * h)
        trayectoria.append(u.copy())
    return np.array(trayectoria)
def runge_kutta_O2(u0, h, cantidad_iteraciones):
    u = u0.copy()
    trayectoria = [u.copy()]
    for n in range(cantidad_iteraciones):
        tn = n * h
        q1 = h * f(u, tn)
        q2 = h * f(u + q1, tn + h)
        u  = u + 0.5 * (q1 + q2)
        trayectoria.append(u.copy())
    return np.array(trayectoria)
def runge_kutta_O4(u0, h, cantidad_iteraciones):
    u = u0.copy()
    trayectoria = [u.copy()]
    for n in range(cantidad_iteraciones):
        tn = n * h
        # Etapa Predictor
        k1 = h * f(u, tn)
        k2 = h * f(u + 0.5 * k1, tn + 0.5 * h)
        k3 = h * f(u + 0.5 * k2, tn + 0.5 * h)
        k4 = h * f(u + k3, tn + h)
        # Etapa Corrector
        u  = u + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        trayectoria.append(u.copy())
        
    return np.array(trayectoria)
# ── Configuración de la Simulación a Largo Plazo ──────────────────
h = 3600.0
dias_simulacion = 180.0  # 6 meses completos para forzar e identificar derivas orbitales 
cantidad_iteraciones = int(dias_simulacion * 24) 
u0 = np.array([x0, y0, vx0, vy0])
print(f"Simulando {dias_simulacion} días con un paso h = {h/3600:.1f} hora...")
vector_trayectoria_euler = euler_explicito(u0, h, cantidad_iteraciones)
vector_trayectoria_rk2   = runge_kutta_O2(u0, h, cantidad_iteraciones)
vector_trayectoria_rk4   = runge_kutta_O4(u0, h, cantidad_iteraciones)
# ── Procesamiento de Distancias ─────────────────────────────────────────
dist_euler = np.sqrt(vector_trayectoria_euler[:, 0]**2 + vector_trayectoria_euler[:, 1]**2) / 1e3
dist_rk2   = np.sqrt(vector_trayectoria_rk2[:, 0]**2 + vector_trayectoria_rk2[:, 1]**2) / 1e3
dist_rk4   = np.sqrt(vector_trayectoria_rk4[:, 0]**2 + vector_trayectoria_rk4[:, 1]**2) / 1e3
tiempo_dias = np.arange(cantidad_iteraciones + 1) * h / 86400.0
# ── Gráfico Comparativo de Estabilidad Exigido ───────────────────────────────
plt.figure(figsize=(12, 6))
plt.plot(tiempo_dias, dist_euler, 'r-', label='Euler Explícito (O1)', alpha=0.4)
plt.plot(tiempo_dias, dist_rk2, 'g-', label='Runge-Kutta O2 (O2)', alpha=0.6)
plt.plot(tiempo_dias, dist_rk4, 'b-', label='Runge-Kutta O4 (O4 - Punto 6)', lw=2)
# Valores de referencia oficiales
plt.axhline(363300, color='black', linestyle='--', alpha=0.4, label='Perigeo Teórico (~363.300 km)')
plt.axhline(405500, color='black', linestyle=':', alpha=0.4, label='Apogeo Teórico (~405.500 km)')
plt.xlabel('Tiempo (días)')
plt.ylabel('Distancia Tierra-Luna (km)')
plt.title('Estabilidad Orbital a Largo Plazo (180 días)\nComparativa: Euler vs RK2 vs RK4')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
# ── Validación de Amplitudes Finales ─────────────────────────────────────────
def reportar_extremos(distancias, nombre):
    print(f"\n[{nombre}] tras {dias_simulacion} días:")
    print(f"  Mínima distancia alcanzada (Perigeo): {distancias.min():.1f} km")
    print(f"  Máxima distancia alcanzada (Apogeo) : {distancias.max():.1f} km")
reportar_extremos(dist_euler, "Euler Explícito")
reportar_extremos(dist_rk2, "Runge-Kutta O2")
reportar_extremos(dist_rk4, "Runge-Kutta O4")