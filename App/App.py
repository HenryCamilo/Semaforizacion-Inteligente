import streamlit as st
import cv2
from Detector import VehicleDetector
from Semaforo import SemaforoConfig, SemaforoController
import time
import tempfile
import os

st.set_page_config(page_title="🚦 Semaforización Inteligente", layout="wide")
st.title("🚦 Semaforización Inteligente")

# ==============================
# Sidebar para selección de fuente
# ==============================
st.sidebar.header("⚙️ Configuración de Fuente de Video")

fuente = st.sidebar.radio(
    "Selecciona la fuente de video:",
    ("📂 Subir Video", "🌐 URL de Cámara", "🎥 Cámara Local")
)

video_path = None

if fuente == "📂 Subir Video":
    archivo_video = st.sidebar.file_uploader("Sube un archivo de video", type=["mp4", "avi", "mov", "mkv"])
    if archivo_video is not None:
        # Guardar en archivo temporal
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp_file.write(archivo_video.read())
        video_path = tmp_file.name

elif fuente == "🌐 URL de Cámara":
    url = st.sidebar.text_input("Introduce la URL (RTSP/HTTP):")
    if url:
        video_path = url

elif fuente == "🎥 Cámara Local":
    cam_index = st.sidebar.number_input("Índice de cámara", min_value=0, step=1, value=0)
    video_path = int(cam_index)

# ==============================
# Inicialización del sistema
# ==============================
config = SemaforoConfig()
semaforo = SemaforoController(config)
detector = VehicleDetector("Models/best.pt")

# ==============================
# Función para correr simulación
# ==============================
def run_simulacion(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("❌ No se pudo abrir la fuente de video")
        return

    frame_placeholder = st.empty()
    col1, col2, col3, col4 = st.columns(4)
    flujo_placeholder = col1.empty()
    verde_placeholder = col2.empty()
    amarillo_placeholder = col3.empty()
    rojo_placeholder = col4.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame, tiempos = detector.procesar_frame(frame, semaforo)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Mostrar video (reducido)
        frame_placeholder.image(frame_rgb, channels="RGB", width=600)

        # Mostrar métricas (se actualizan en el mismo lugar)
        flujo_placeholder.metric("🚗 Flujo", tiempos["flujo"])
        verde_placeholder.metric("🟢 Verde", tiempos["verde"])
        amarillo_placeholder.metric("🟡 Amarillo", tiempos["amarillo"])
        rojo_placeholder.metric("🔴 Rojo", tiempos["rojo"])

        time.sleep(0.08)

    cap.release()


# ==============================
# Botón para iniciar
# ==============================
if video_path is not None:
    if st.button("▶️ Iniciar Simulación"):
        run_simulacion(video_path)
else:
    st.info("ℹ️ Selecciona primero una fuente de video en la barra lateral")

