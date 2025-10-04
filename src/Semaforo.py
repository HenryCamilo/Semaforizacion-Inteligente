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
        # Solo recalcular si pasaron al menos update_interval segundos
        if now - self.last_update >= self.config.update_interval:
            flujo = self.contador_bloque

            if 0 <= flujo <= 2:
                verde = self.config.t_default
            elif 3 <= flujo <= 7:
                verde = self.config.t_min
            elif 8 <= flujo <= 15:
                verde = int(self.config.t_min + (flujo - 5) * ((self.config.t_default - self.config.t_min) / 10))
            else:
                verde = self.config.t_max

            amarillo = self.config.t_yellow
            rojo = self.config.ciclo_total - (verde + amarillo)

            self.last_tiempos = {"flujo": flujo, "verde": verde, "amarillo": amarillo, "rojo": rojo}
            self.last_update = now  
            self.contador_bloque = 0

        #Mientras no pasen 8s, se devuelve el último valor
        return self.last_tiempos

