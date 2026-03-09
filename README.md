# Detección de Círculos e Imperfecciones

Un programa en **Python** que detecta círculos en imágenes y analiza imperfecciones dentro de ellos. Ideal para **control de calidad**, inspección visual automatizada y análisis de piezas circulares.

---

## 📂 Estructura del Proyecto

```
.
├── main.py                       # Script principal de detección
├── config.py                     # Parámetros y configuración
├── generar_csv_mediciones.py     # Generador de reportes CSV
├── detection/
│   ├── __init__.py
│   ├── circle_detection.py       # Detección de círculos
│   └── defect_detection.py       # Detección de defectos
├── processing/
│   ├── __init__.py
│   ├── image_processing.py       # Procesamiento de imágenes
│   └── utils.py                  # Utilidades de guardado y visualización
├── imagenesentrada/
│   ├── Entrada/                  # Imágenes de entrada
│   ├── Entrada_sincriogenia/     # Entrada sin criogenia
│   ├── Salida/                   # Imágenes de salida
│   └── Salida_sincriogenia/      # Salida sin criogenia
├── Capturas_Procesadas/          # Resultados procesados
├── README.md                     # Documentación
└── LICENSE                       # Licencia MIT
```

---

## ⚡ Características

* **Detección de círculos** mediante HoughCircles híbrido con fallback por contornos
* **Detección de defectos** dentro del círculo (manchas, rasguños, imperfecciones)
* **Visualización y guardado** de resultados con líneas de colores:

  * **Verde** → círculo detectado
  * **Rojo** → centro y contornos de defectos
* **Generación de reportes CSV** con métricas de perímetros
* **Optimización automática** para imágenes grandes (redimensionamiento)
* **Timeout y filtros** para imágenes problemáticas o con mucho ruido

---

## 🛠 Requisitos

* Python 3.7+
* OpenCV (`cv2`)
* NumPy (`np`)

Instalación rápida:

```bash
pip install opencv-python numpy
```

---

## 🚀 Cómo usar

### 1️⃣ Procesar imágenes de ejemplo

Esta rama incluye imágenes de ejemplo en `imagenesentrada/`.

```bash
python main.py
```

* Todas las imágenes se procesan y se guardan en `Capturas_Procesadas/`.
* Se muestran en pantalla los resultados con imperfecciones marcadas.

### 2️⃣ Procesar tus propias imágenes

1. Coloca tus imágenes `.jpg` en cualquiera de estas carpetas:

   * `imagenesentrada/Entrada/`
   * `imagenesentrada/Entrada_sincriogenia/`
   * `imagenesentrada/Salida/`
   * `imagenesentrada/Salida_sincriogenia/`

2. Ejecuta:

```bash
python main.py
```

### 3️⃣ Generar reporte CSV

Después de procesar imágenes, genera métricas:

```bash
python generar_csv_mediciones.py
```

* Crea `Capturas_Procesadas/resultados_perimetros.csv` con:

  * Nombre de la imagen
  * Perímetro del círculo (verde)
  * Perímetro total de defectos (rojo)

---

## ⚙ Configuración

Edita `config.py` para ajustar la detección:

```python
params = {
    'blur_kernel': 15,          # Desenfoque para reducir ruido
    'draw_fraction': 0.95,      # Fracción del radio dibujado
    'min_defect_area': 200,     # Área mínima para defectos
    'defect_threshold': 12,     # Sensibilidad de defectos
    'canny_low': 50,            # Límite bajo Canny
    'canny_high': 150           # Límite alto Canny
}

params_hough = {
    'dp': 1.2,
    'param1': 100,
    'param2': 25,
    'minRadius_factor': 0.12,
    'maxRadius_factor': 0.50
}
```

* Ajusta **`blur_kernel`** si las imágenes tienen mucho ruido
* Ajusta **`min_defect_area`** si detecta demasiados falsos positivos
* Ajusta **`defect_threshold`** para mejorar sensibilidad

---

## 🔧 Funciones clave

* `process_image(path, prefix="")` → Procesa una imagen individual y guarda resultados
* `detect_circles_fast(img)` → Detecta círculos con redimensionamiento optimizado
* `detect_circles_hybrid(img)` → Método híbrido con varios algoritmos de Hough
* `detect_imperfections(img, x, y, r)` → Detecta imperfecciones dentro del círculo
* `save_images(img, base_name, extra="")` → Guarda imágenes procesadas
* `calcular_metricas(path)` → Calcula perímetros para CSV

---

## 🛠 Troubleshooting

| Problema                | Solución                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------ |
| Círculo no se detecta   | Ajusta `defect_threshold`, `min_defect_area` o verifica que el círculo esté centrado |
| Muchos falsos positivos | Aumenta `min_defect_area` o `defect_threshold`                                       |
| Proceso lento           | Reducir resolución original o ajustar parámetros Hough para menos precisión          |

---

## 📄 Licencia

MIT License — libre para uso personal y académico.
