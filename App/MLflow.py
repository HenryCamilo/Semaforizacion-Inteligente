import mlflow
import mlflow.pyfunc
import time
from Semaforo import SemaforoConfig, SemaforoController #Recuerde que esta en la carpeta src
from Detector import VehicleDetector #Recuerde que esta en la carpeta src
from Display import Display #Recuerde que esta en la carpeta src
import cv2

if __name__ == "__main__":
    MODEL_PATH = r"C:\Users\Camil\Desktop\Especializacion 2do semestre\Proyecto de IA\Proyecto semaforizacion\Models\best.pt"
    VIDEO_PATH = r"C:\Users\Camil\Desktop\Especializacion 2do semestre\Proyecto de IA\Proyecto semaforizacion\video de prueba\Cali de noche en su tráfico  #viralvideo #shorts #videoshorts #shortvideo.mp4"

    # Inicia experimento en MLflow
    mlflow.set_experiment("semaforizacion_inteligente")

    with mlflow.start_run():
        # --- Log params (configuración inicial) ---
        config = SemaforoConfig()
        mlflow.log_param("t_min", config.t_min)
        mlflow.log_param("t_max", config.t_max)
        mlflow.log_param("t_default", config.t_default)
        mlflow.log_param("conf_yolo", 0.3)

        semaforo = SemaforoController(config)
        detector = VehicleDetector(MODEL_PATH)

        cap = cv2.VideoCapture(VIDEO_PATH)
        frame_count, vehiculos_totales = 0, 0
        start = time.time()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            frame = detector.procesar_frame(frame, semaforo)
            tiempos = semaforo.calcular_tiempos()
            vehiculos_totales += tiempos["flujo"]

        cap.release()

        duracion = time.time() - start
        fps = frame_count / duracion
        flujo_promedio = vehiculos_totales / max(1, frame_count)

        # --- Log metrics (resultados del run) ---
        mlflow.log_metric("fps", fps)
        mlflow.log_metric("flujo_promedio", flujo_promedio)
        mlflow.log_metric("verde_medio", tiempos["verde"])
        mlflow.log_metric("amarillo_medio", tiempos["amarillo"])
        mlflow.log_metric("rojo_medio", tiempos["rojo"])

        # --- Log artifacts ---
        mlflow.log_artifact(VIDEO_PATH, artifact_path="input_video")
        mlflow.log_artifact(MODEL_PATH, artifact_path="model")

        print(f"Run registrado en MLflow con fps={fps:.2f}, flujo={flujo_promedio:.2f}")

