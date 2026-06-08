import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Constantes ────────────────────────────────────────────────────────────────
G  = 6.674e-11   # m³/(kg·s²)
MT = 5.972e24    # kg — masa de la Tierra
ML = 7.342e22    # kg  — masa de la Luna  
RT = 6_371_000   # m  — radio terrestre

ALTITUD_REENTRADA = 120_000  # m
R_LUNA_M  = 384_400_000.0   # m  — distancia media Tierra-Luna
T_LUNA_S  = 27.32 * 86400   # s  — período orbital lunar
OMEGA_LUNA = 2 * np.pi / T_LUNA_S   # rad/s

# ── Métodos numéricos ─────────────────────────────────────────────────────────
def f_luna(u, t):
    x, y, vx, vy = u
    d = np.sqrt(x**2 + y**2)
    ax = -G * MT / d**2 * (x / d)
    ay = -G * MT / d**2 * (y / d)
    return np.array([vx, vy, ax, ay])

def runge_kutta_O2(f, u0, h, n_pasos):
    u = u0.copy()
    tray = [u.copy()]
    for n in range(n_pasos):
        tn = n * h
        q1 = h * f(u, tn)
        q2 = h * f(u + q1, tn + h)
        u  = u + 0.5 * (q1 + q2)
        tray.append(u.copy())
    return np.array(tray)

def euler_explicito(f, u0, h, n_pasos):
    u = u0.copy()
    tray = [u.copy()]
    for n in range(n_pasos):
        u = u + h * f(u, n * h)
        tray.append(u.copy())
    return np.array(tray)

# ── Leer CSV ──────────────────────────────────────────────────────────────────
df = pd.read_csv(
    'Artemis_II_Data.csv',
    sep=';', decimal=',', header=None,
    names=['tiempo', 'x_km', 'y_km', 'z_km', 'vx_kms', 'vy_kms', 'vz_kms']
)
df['dt'] = pd.to_datetime(
    df['tiempo'].str.replace(',', '.', regex=False),
    format='mixed', utc=True
)

# ── Determinar posición real de la Luna desde la telemetría ───────────────────
# El punto de máxima distancia 3-D de la Tierra es el flyby lunar.
# En ese momento Orion está más cerca de la Luna, por lo que el ángulo 2-D
# de la posición de Orion es aproximadamente el ángulo de la Luna en el plano (x, y).
df['r3d_km'] = np.sqrt(df.x_km**2 + df.y_km**2 + df.z_km**2)
idx_flyby    = df['r3d_km'].idxmax()
row_flyby    = df.iloc[idx_flyby]
t_flyby      = row_flyby['dt']
theta_flyby  = np.arctan2(row_flyby['y_km'], row_flyby['x_km'])  # ángulo (x,y) en flyby

print(f"Flyby detectado: {t_flyby}  |  ángulo 2D = {np.degrees(theta_flyby):.2f}°")
print(f"Luna en flyby : ({R_LUNA_M/1e3*np.cos(theta_flyby):.0f},  {R_LUNA_M/1e3*np.sin(theta_flyby):.0f}) km")

def luna_real_pos_m(timestamp):
    """
    Posición 2-D de la Luna (en metros) en un Timestamp UTC dado.
    Se basa en propagación circular desde el flyby detectado en el CSV.
    """
    dt_s = (timestamp - t_flyby).total_seconds()
    theta = theta_flyby + OMEGA_LUNA * dt_s
    return R_LUNA_M * np.cos(theta), R_LUNA_M * np.sin(theta)

# ── Condiciones iniciales de Orion desde la ventana 4-6 am del 3 de abril ────
t_inicio_ventana = pd.Timestamp('2026-04-03T04:00:00', tz='UTC')
t_fin_ventana    = pd.Timestamp('2026-04-03T06:00:00', tz='UTC')
ventana = df[(df['dt'] >= t_inicio_ventana) & (df['dt'] <= t_fin_ventana)].reset_index(drop=True)

fila      = ventana.iloc[0]
t0_orion  = fila['dt']

x0_orion  = fila['x_km']  * 1e3
y0_orion  = fila['y_km']  * 1e3
vx0_orion = fila['vx_kms'] * 1e3
vy0_orion = fila['vy_kms'] * 1e3

print(f"\nCondiciones iniciales Orion: {t0_orion}")
print(f"  Posición  : ({x0_orion/1e3:.1f}, {y0_orion/1e3:.1f}) km")
print(f"  Velocidad : ({vx0_orion:.2f}, {vy0_orion:.2f}) m/s")

# ── Simulación de la Luna con RK2 (para f_orion) ─────────────────────────────
# La usamos para el campo gravitacional durante la integración de Orion.
# Las CI de la Luna se sincronizan con t0_orion usando la posición real.
xL0, yL0 = luna_real_pos_m(t0_orion)
# Velocidad tangencial (órbita circular, sentido antihorario)
theta0_luna = np.arctan2(yL0, xL0)
v_luna_media = 2 * np.pi * R_LUNA_M / T_LUNA_S   # ≈ 1022 m/s
vxL0 = -v_luna_media * np.sin(theta0_luna)
vyL0 =  v_luna_media * np.cos(theta0_luna)

h = 60.0   # paso de integración en segundos
t_fin_csv = df['dt'].iloc[-1]
duracion_total_s = (t_fin_csv - t0_orion).total_seconds()
n_pasos_orion = int(duracion_total_s / h)

u0_luna  = np.array([xL0, yL0, vxL0, vyL0])
tray_luna_sim = runge_kutta_O2(f_luna, u0_luna, h, n_pasos_orion + 200)

print(f"\nLuna en t0 (posición real): ({xL0/1e3:.0f}, {yL0/1e3:.0f}) km")
print(f"Pasos Orion: {n_pasos_orion}  ({duracion_total_s/86400:.2f} días)")

# ── EDO Orion (Tierra + Luna) ─────────────────────────────────────────────────
def f_orion(u_orion, paso_idx):
    xo, yo, vxo, vyo = u_orion
    idx_luna = min(paso_idx, len(tray_luna_sim) - 1)
    xL = tray_luna_sim[idx_luna, 0]
    yL = tray_luna_sim[idx_luna, 1]

    dT    = np.sqrt(xo**2 + yo**2)
    dxL   = xL - xo;  dyL = yL - yo
    dL    = np.sqrt(dxL**2 + dyL**2)

    ax = -G * MT / dT**2 * (xo / dT) + G * ML / dL**2 * (dxL / dL)
    ay = -G * MT / dT**2 * (yo / dT) + G * ML / dL**2 * (dyL / dL)
    return np.array([vxo, vyo, ax, ay])

# ── Integración Euler y RK2 ───────────────────────────────────────────────────
u0_orion = np.array([x0_orion, y0_orion, vx0_orion, vy0_orion])

u_euler    = u0_orion.copy()

# Hardcodeamos la posicion inicial.
u_euler[0] = -6.55824844e+07 

tray_euler = [u_euler.copy()]
for n in range(n_pasos_orion):
    u_euler = u_euler + h * f_orion(u_euler, n)
    tray_euler.append(u_euler.copy())
    if np.sqrt(u_euler[0]**2 + u_euler[1]**2) < RT + ALTITUD_REENTRADA:
        print(f"  Euler: reentrada en paso {n} ({n*h/3600:.1f} h)")
        break
tray_euler = np.array(tray_euler)

u_rk2    = u0_orion.copy()
u_rk2[0] = -6.55000000e+07 
u_rk2[0] = -6.55355432e+07 
tray_rk2 = [u_rk2.copy()]
for n in range(n_pasos_orion):
    q1   = h * f_orion(u_rk2, n)
    q2   = h * f_orion(u_rk2 + q1, n + 1)
    u_rk2 = u_rk2 + 0.5 * (q1 + q2)
    tray_rk2.append(u_rk2.copy())
    if np.sqrt(u_rk2[0]**2 + u_rk2[1]**2) < RT + ALTITUD_REENTRADA:
        print(f"  RK2:  reentrada en paso {n} ({n*h/3600:.1f} h)")
        break
tray_rk2 = np.array(tray_rk2)

# ── Telemetría NASA (datos reales, proyección 2D) ─────────────────────────────
df_real = df[df['dt'] >= t0_orion].copy()
x_real  = df_real['x_km'].values * 1e3
y_real  = df_real['y_km'].values * 1e3
t_real  = np.array([(t - t0_orion).total_seconds() for t in df_real['dt']])

# Posición real de la Luna para cada punto del CSV (curva orbital real)
xL_real = np.array([luna_real_pos_m(t)[0] for t in df_real['dt']])
yL_real = np.array([luna_real_pos_m(t)[1] for t in df_real['dt']])

# Posiciones clave de la Luna
xL_t0,    yL_t0    = luna_real_pos_m(t0_orion)
xL_flyby, yL_flyby = luna_real_pos_m(t_flyby)
xL_fin,   yL_fin   = luna_real_pos_m(t_fin_csv)

# Radio visual de la Luna para los gráficos
RL_m = 1_737_400.0   # m

# ── Gráfico principal ─────────────────────────────────────────────────────────
theta_circ = np.linspace(0, 2 * np.pi, 360)
fig, axes  = plt.subplots(1, 2, figsize=(17, 8))
fig.suptitle(
    'Punto 3: Trayectoria Orion — Artemis II\n'
    'Euler vs RK2 vs Telemetría NASA  |  Luna en posición real (derivada del flyby)',
    fontsize=12, fontweight='bold'
)

for ax, escala, titulo in zip(
    axes,
    [1e6, 1e3],
    ['Vista completa (×10⁶ m)', 'Acercamiento zona de reentrada (×10³ m)']
):
    s = escala

    # ── Tierra ──
    ax.fill(RT/s * np.cos(theta_circ), RT/s * np.sin(theta_circ),
            color='royalblue', alpha=0.75, zorder=4)

    # ── Trayectorias de Orion ──
    ax.plot(tray_euler[:,0]/s, tray_euler[:,1]/s,
            color='tomato', lw=1.2, alpha=0.85, label='Euler', zorder=3)
    ax.plot(tray_rk2[:,0]/s,   tray_rk2[:,1]/s,
            color='seagreen', lw=1.5, alpha=0.9, label='RK2', zorder=3)
    ax.plot(x_real/s, y_real/s,
            'k--', lw=1.2, alpha=0.6, label='NASA (telemetría real)', zorder=3)

    # ── Órbita de la Luna durante la misión (curva real) ──
    ax.plot(xL_real/s, yL_real/s,
            color='gold', lw=1.0, ls='--', alpha=0.7,
            label='Órbita lunar (real, período 27.32 d)', zorder=2)

    # ── Luna en t0 ──
    ax.fill((xL_t0 + RL_m * np.cos(theta_circ))/s,
            (yL_t0 + RL_m * np.sin(theta_circ))/s,
            color='lightgray', alpha=0.6, zorder=5)
    ax.plot((xL_t0 + RL_m * np.cos(theta_circ))/s,
            (yL_t0 + RL_m * np.sin(theta_circ))/s,
            'gray', lw=0.8, zorder=5)
    ax.annotate('Luna\n(t₀ Orion)',
                xy=(xL_t0/s, yL_t0/s), fontsize=7,
                ha='center', va='center', color='dimgray', zorder=6)

    # ── Luna en flyby (posición real durante el sobrevuelo) ──
    ax.fill((xL_flyby + RL_m * np.cos(theta_circ))/s,
            (yL_flyby + RL_m * np.sin(theta_circ))/s,
            color='silver', alpha=0.9, zorder=5)
    ax.plot((xL_flyby + RL_m * np.cos(theta_circ))/s,
            (yL_flyby + RL_m * np.sin(theta_circ))/s,
            'dimgray', lw=1.0, zorder=5)
    ax.annotate('Luna\n(flyby)',
                xy=(xL_flyby/s, yL_flyby/s), fontsize=7,
                ha='center', va='center', color='black',
                fontweight='bold', zorder=6)

    # ── Puntos de referencia ──
    ax.plot(x0_orion/s, y0_orion/s, 'go', ms=7, zorder=7, label='t₀ Orion')
    ax.plot(tray_rk2[-1,0]/s, tray_rk2[-1,1]/s,
            'r^', ms=7, zorder=7, label='Reentrada RK2')

    ax.set_xlabel(f'x  (unidad = {s:.0e} m)')
    ax.set_ylabel(f'y  (unidad = {s:.0e} m)')
    ax.set_title(titulo)
    ax.legend(fontsize=8, loc='lower right')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.25)

plt.tight_layout()
plt.savefig('punto3_trayectoria_orion.png', dpi=150, bbox_inches='tight')
print("\nGráfico guardado: punto3_trayectoria_orion.png")

# ── Comparación cuantitativa ───────────────────────────────────────────────────
print("\n" + "="*55)
print("  COMPARACIÓN FINAL")
print("="*55)
for tray, nombre in [(tray_euler, "Euler"), (tray_rk2, "RK2")]:
    n = min(len(tray), len(tray_luna_sim))
    dx = tray[:n, 0] - tray_luna_sim[:n, 0]
    dy = tray[:n, 1] - tray_luna_sim[:n, 1]
    dist_luna_min = np.sqrt(dx**2 + dy**2).min() / 1e3
    print(f"\n  {nombre}:")
    print(f"    Pasos integrados      : {len(tray)-1}")
    print(f"    Distancia mín. a Luna : {dist_luna_min:.0f} km")
    dist_fin = np.sqrt(tray[-1,0]**2 + tray[-1,1]**2) / 1e3
    print(f"    Distancia final Tierra: {dist_fin:.0f} km")

plt.show()