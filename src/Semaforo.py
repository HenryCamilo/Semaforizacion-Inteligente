import time
from collections import deque

class SemaforoConfig:
    def __init__(self, t_min=12, t_max=50, t_default=10, t_yellow=3, ciclo_total=90, update_interval=4):
        self.t_min = t_min
        self.t_max = t_max
        self.t_default = t_default
        self.t_yellow = t_yellow
        self.ciclo_total = ciclo_total
        self.update_interval = update_interval 


class SemaforoController:
    def __init__(self, config: SemaforoConfig):
        self.config = config
        self.contador_bloque = 0 
        self.last_update = time.time()
        self.last_tiempos = {"flujo": 0, "verde": config.t_default,
                            "amarillo": config.t_yellow,
                            "rojo": config.ciclo_total - (config.t_default + config.t_yellow)}

    def registrar_paso(self):
        self.contador_bloque += 1

    def calcular_tiempos(self):
        now = time.time()
        if now - self.last_update >= self.config.update_interval:
            flujo = self.contador_bloque
            duracion = now - self.last_update if self.last_update > 0 else self.config.update_interval
            velocidad_flujo = flujo / duracion  # veh/s

            # Análisis de condiciones
            if flujo == 0:
                # No hay carros: semáforo normal
                verde = self.config.t_default

            elif velocidad_flujo > 0.8:
                # Muchos carros, pero flujo rápido (tráfico fluido)
                verde = self.config.t_default

            elif 0.2 <= velocidad_flujo <= 0.8:
                # Flujo medio: se ajusta ligeramente hacia arriba
                incremento = int((velocidad_flujo - 0.2) * (self.config.t_max - self.config.t_default))
                verde = self.config.t_default + incremento

            else:
            # Flujo lento (acumulación o congestión)
                verde = self.config.t_max

            # Límites
            verde = max(self.config.t_min, min(verde, self.config.t_max))

            amarillo = self.config.t_yellow
            rojo = self.config.ciclo_total - (verde + amarillo)

            self.last_tiempos = {
                "flujo": flujo,
                "velocidad_flujo": round(velocidad_flujo, 2),
                "verde": verde,
                "amarillo": amarillo,
                "rojo": rojo
            }

            self.last_update = now
            self.contador_bloque = 0

        
        return self.last_tiempos


