# Semaforizacion-Inteligente

# Sistema de Semaforización Inteligente con Visión por Computador y Streamlit

Este proyecto implementa un **sistema de control de semáforos inteligente** basado en visión por computador.  
Utiliza **YOLOv8** para el conteo de vehículos, **MLflow** para el registro de experimentos, y una interfaz en **Streamlit** que permite visualizar el video procesado junto con los datos de flujo vehicular y tiempos semafóricos en tiempo real.

---

## Descripción general

El sistema simula un semáforo que **ajusta automáticamente el tiempo de luz verde** en función del tráfico detectado.  
A mayor congestión, el tiempo verde aumenta; si el flujo es fluido o bajo, los tiempos se mantienen o disminuyen, optimizando el tránsito de forma dinámica.


## Características principales

- **Detección de vehículos** usando YOLOv12.  
- **Conteo de flujo vehicular bidireccional** (norte–sur y sur–norte).  
- **Control adaptativo** del tiempo verde, amarillo y rojo según el flujo.  
- **Registro de métricas y resultados** mediante MLflow.  
- **Interfaz visual en Streamlit** para observar el video, el conteo y los tiempos del semáforo en tiempo real.  
- **Pruebas automáticas** con `pytest` para verificar la lógica de cálculo.


## Estructura del proyecto
│
├── App.py # Interfaz en Streamlit
├── Main.py # Script principal que ejecuta el flujo completo
├── MLflow.py # Registro de experimentos y métricas
├── Detector.py # Detección y conteo de vehículos
├── Display.py # Visualización en video (OpenCV)
├── Semaforo.py # Control inteligente de tiempos del semáforo
├── test_Pytest.py # Pruebas automáticas
├── check_gpu.py # Verificación de compatibilidad GPU
├── requirements.txt # Dependencias del proyecto
├── best.pt # Modelo usado
├── yolo12n.pt # Modelo YOLO que se uso para entrenar el best.pt
└── Proyecto-jupyter.ipynb # Análisis y experimentos previos

Recordar que despues de crear el ambiente intealar el requirements.txt 

### Contribuciones 

¡Toda contribución es bienvenida!
Si deseas mejorar el modelo, la interfaz o añadir métricas de tráfico más avanzadas, realiza un pull request o abre un issue.

## Autor

### Henry Camilo Valencia
Ingeniero Biomédico con interés en visión por computador, inteligencia artificial y automatización.
📧 camiloh8595@outlook.com


