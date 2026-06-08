import numpy as np

# ── Constantes ────────────────────────────────────────────────────────────────
G  = 6.674e-11        # m³/(kg·s²)
MT = 5.972e24         # kg  — masa de la Tierra
 
# Condiciones iniciales de la Luna
# Perigeo: 363300 km, velocidad perpendicular al eje x
x0  =  363300000      # m   (perigeo sobre eje +x)
y0  =  0.0
vx0 =  0.0
vy0 =  1_076.0        # m/s (velocidad en perigeo, dirección +y)

# ── Métodos numéricos ─────────────────────────────────────────────────────────
def f(u, t):
    x, y, vx, vy = u
    dT = np.sqrt(x**2 + y**2)          # distancia Tierra-Luna por pitagoras
    alpha = np.arctan2(y, x)           # ángulo desde la Tierra hacia la Luna
 
    # La gravedad de la Tierra atrae a la Luna, por eso el signo negativo
    ax = -G * MT / dT**2 * np.cos(alpha)
    ay = -G * MT / dT**2 * np.sin(alpha)
 
    return np.array([vx, vy, ax, ay])

def euler_explicito(u0, h, cantidad_iteraciones):
    u = u0.copy()
    vectoria_trayectoria = [u.copy()]
 
    for n in range(cantidad_iteraciones):
        u = u + h * f(u, n * h)
        vectoria_trayectoria.append(u.copy())
 
    return np.array(vectoria_trayectoria)

def runge_kutta_O2(u0, h, cantidad_iteraciones):
    u = u0.copy()
    vectoria_trayectoria = [u.copy()]
 
    for n in range(cantidad_iteraciones):
        tn = n * h
        q1 = h * f(u, tn)
        q2 = h * f(u + q1, tn + h)
        u  = u + 0.5 * (q1 + q2)
        vectoria_trayectoria.append(u.copy())
 
    return np.array(vectoria_trayectoria)

# ── Determinar la orbita lunar ───────────────────
h = 3600.0            # 1 hora en segundos
dias = 27.3           # período orbital de la Luna
cantidad_iteraciones = int(dias * 24)    # número de pasos para una órbita completa
 
u0 = np.array([x0, y0, vx0, vy0])
 
vector_trayectoria_euler = euler_explicito(u0, h, cantidad_iteraciones)
vector_trayectoria_rk2   = runge_kutta_O2(u0, h, cantidad_iteraciones)

def validar(vector_trayectoria, nombre):
    x  = vector_trayectoria[:, 0]
    y  = vector_trayectoria[:, 1]
    vx = vector_trayectoria[:, 2]
    vy = vector_trayectoria[:, 3]
 
    distancias  = np.sqrt(x**2 + y**2) / 1e3   # km
    velocidades = np.sqrt(vx**2 + vy**2) / 1e3  # km/s
 
    print(f"\n{'='*45}")
    print(f"  VALIDACIÓN — {nombre}")
    print(f"{'='*45}")
    print(f"  Perigeo  simulado : {distancias.min():.1f} km   (esperado ≈ 363300 km)")
    print(f"  Apogeo   simulado : {distancias.max():.1f} km   (esperado ≈ 405500 km)")
    print(f"  Vel. máxima       : {velocidades.max():.4f} km/s (esperado ≈ 1.076 km/s)")
    print(f"  Vel. mínima       : {velocidades.min():.4f} km/s (esperado ≈ 0.963 km/s)")
 
validar(vector_trayectoria_euler, "Euler Explícito")
validar(vector_trayectoria_rk2,   "Runge-Kutta O2")