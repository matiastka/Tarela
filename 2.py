import pandas as pd
import numpy as np

df = pd.read_csv(
    'Artemis_II_Data.csv',
    sep=';',
    decimal=',',
    header=None,
    names=['tiempo', 'x_km', 'y_km', 'z_km', 'vx_kms', 'vy_kms', 'vz_kms']
)
 
print("Datos Cargados")
print(f"Total de filas: {len(df)}")
print(f"Primer tiempo: {df['tiempo'].iloc[0]}")
print(f"Último tiempo: {df['tiempo'].iloc[-1]}")

mask_ventana = df['tiempo'].apply(
    lambda t: '2026-04-03T04' <= t[:13] <= '2026-04-03T05'
)
ventana = df[mask_ventana].reset_index(drop=True)
 
print(f"\nRango entre las 4am a 6am del 3 de abril")
print(f"Filas disponibles  : {len(ventana)}")
print(ventana[['tiempo', 'x_km', 'y_km', 'vx_kms', 'vy_kms']].to_string())

fila_elegida = ventana.iloc[0]
 
# Pasar de km a m  y  km/s a m/s
x0  = fila_elegida['x_km']  * 1e3   # m
y0  = fila_elegida['y_km']  * 1e3   # m
vx0 = fila_elegida['vx_kms'] * 1e3  # m/s
vy0 = fila_elegida['vy_kms'] * 1e3  # m/s
 
# Magnitudes para verificación
distancia_tierra = np.sqrt(x0**2 + y0**2)          # m
velocidad_total  = np.sqrt(vx0**2 + vy0**2)        # m/s
 
print(f"\nCondiciones inciales elegidas")
print(f"tiempo: {fila_elegida['tiempo']}")
print(f"x0: {x0:.2f} m  ({x0/1e3:.1f} km)")
print(f"y0: {y0:.2f} m  ({y0/1e3:.1f} km)")
print(f"vx0: {vx0:.4f} m/s  ({vx0/1e3:.4f} km/s)")
print(f"vy0: {vy0:.4f} m/s  ({vy0/1e3:.4f} km/s)")
print(f"\nDistancia a la Tierra Inicial: {distancia_tierra:.2f} m  ({distancia_tierra/1e3:.1f} km)")
print(f"Velocidad total: {velocidad_total:.4f} m/s  ({velocidad_total/1e3:.4f} km/s)")

u0_orion = np.array([x0, y0, vx0, vy0])
print(f"\nVector u0 para integrador")
print(f"u0 = {u0_orion}")