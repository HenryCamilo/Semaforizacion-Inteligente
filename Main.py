import time
import cv2
from Detector import VehicleDetector #Recuerde que esta en la carpeta src
from Semaforo import SemaforoConfig, SemaforoController #Recuerde que esta en la carpeta src
from Display import Display#Recuerde que esta en la carpeta src

VIDEO_PATH = r"Supropio_video.mp4"
MODEL_PATH = r"Model/best.pt"

def main():
    config = SemaforoConfig()
    semaforo = SemaforoController(config)
    detector = VehicleDetector(MODEL_PATH, conf=0.3, line_y=300)
    display = Display()

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir video: {VIDEO_PATH}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame, tiempos = detector.procesar_frame(frame, semaforo)
        display.mostrar(frame, tiempos)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

