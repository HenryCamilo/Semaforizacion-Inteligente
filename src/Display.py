import cv2

class Display:
    def mostrar(self, frame, tiempos):
        flujo, verde, amarillo, rojo = tiempos["flujo"], tiempos["verde"], tiempos["amarillo"], tiempos["rojo"]

        cv2.putText(frame, f"Flujo: {flujo} vehs", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
        cv2.putText(frame, f"Verde: {verde}s", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.putText(frame, f"Amarillo: {amarillo}s", (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
        cv2.putText(frame, f"Rojo: {rojo}s", (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        cv2.imshow("Conteo y Semaforo", frame)
