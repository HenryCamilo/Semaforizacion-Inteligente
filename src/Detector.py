import cv2
from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path, conf=0.3, line_y=300):
        self.model = YOLO(model_path)
        self.conf = conf
        self.line_y = line_y
        self.track_memory = {}
        self.total_count = 0
        self.north_count = 0
        self.south_count = 0

    def procesar_frame(self, frame, semaforo):
        results = self.model.track(frame, persist=True, conf=self.conf)

        for r in results:
            for b in r.boxes:
                x1, y1, x2, y2 = map(int, b.xyxy[0].tolist())
                id_ = int(b.id[0]) if b.id is not None else None
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

                if id_ is not None:
                    last_pos = self.track_memory.get(id_)
                    self.track_memory[id_] = (cx, cy)

                    if last_pos:
                        if last_pos[1] < self.line_y <= cy:
                            self.south_count += 1
                            self.total_count += 1
                            semaforo.registrar_paso()
                        elif last_pos[1] > self.line_y >= cy:
                            self.north_count += 1
                            self.total_count += 1
                            semaforo.registrar_paso()

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

        cv2.line(frame, (0, self.line_y), (frame.shape[1], self.line_y), (255, 0, 0), 2)

        tiempos = semaforo.calcular_tiempos()
        return frame, tiempos
