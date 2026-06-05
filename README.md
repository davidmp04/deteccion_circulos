# 🔍 Detección de Círculos e Imperfecciones

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Un sistema profesional en **Python** para **detectar círculos en imágenes** y **analizar imperfecciones** dentro de ellos. Diseñado para **control de calidad industrial**, **inspección visual automatizada** y **análisis de piezas circulares**.

---

## 📌 ¿Qué Hace Este Proyecto?

Este software realiza automáticamente:

1. **Detección de Círculos** 🎯
   - Identifica círculos en imágenes usando el algoritmo de **Transformada de Hough**
   - Dibuja el contorno del círculo detectado en verde
   - Calcula el perímetro y diámetro del círculo

2. **Detección de Defectos** 🔴
   - Identifica imperfecciones (manchas, rasguños, grietas) dentro del círculo
   - Dibuja los defectos en rojo para visualización
   - Calcula el perímetro total de defectos

3. **Análisis y Reportes** 📊
   - Genera archivos **CSV** con métricas de cada imagen
   - Procesa lotes de imágenes automáticamente
   - Organiza resultados por carpetas

---

## 💡 Casos de Uso

- ✅ **Control de Calidad**: Detectar imperfecciones en piezas circulares
- ✅ **Inspección Visual**: Automatizar revisión de manufactura
- ✅ **Análisis de Imágenes**: Procesar lotes de fotos industriales
- ✅ **Metrología**: Medir círculos y defectos automáticamente
- ✅ **Documentación**: Generar reportes de calidad

---

## 🚀 Instalación Rápida

### 1️⃣ Requisitos Previos
- **Python 3.7 o superior**
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

### 2️⃣ Clona el Repositorio
```bash
git clone https://github.com/davidmp04/deteccion_circulos.git
cd deteccion_circulos
```

### 3️⃣ Crea un Entorno Virtual (Recomendado)

**En Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**En Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4️⃣ Instala Dependencias
```bash
pip install -r requirements.txt
```

Si no existe `requirements.txt`, instala manualmente:
```bash
pip install opencv-python numpy
```

---

## 📂 Estructura del Proyecto

```
deteccion_circulos/
│
├── 📄 main.py                          # Script principal - EJECUTA ESTO
├── 📄 config.py                        # Configuración y parámetros
├── 📄 README.md                        # Documentación (este archivo)
├── 📄 LICENSE                          # Licencia MIT
│
├── 📁 detection/                       # Módulo de detección
│   ├── __init__.py
│   ├── circle_detection.py             # Detección de círculos (Hough)
│   └── defect_detection.py             # Detección de defectos y imperfecciones
│
├── 📁 processing/                      # Módulo de procesamiento
│   ├── __init__.py
│   ├── image_processing.py             # Pipeline de procesamiento de imágenes
│   ├── csv_utils.py                    # Generación de reportes CSV
│   └── utils.py                        # Funciones auxiliares
│
├── 📁 imagenesentrada/                 # 📥 AQUÍ COLOCAS TUS IMÁGENES
│   ├── nuevas/
│   │   ├── C1/
│   │   │   ├── TOP/                    # Imágenes de arriba
│   │   │   └── BOTTOM/                 # Imágenes de abajo
│   │   ├── C2/
│   │   └── C3/
│   └── ...
│
└── 📁 Capturas_Procesadas/             # 📤 RESULTADOS (SE CREA AUTOMÁTICAMENTE)
    ├── nuevas/
    │   ├── C1/
    │   │   ├── TOP/
    │   │   │   ├── resultado_imagen1.jpg
    │   │   │   ├── resultado_imagen2.jpg
    │   │   │   └── resultados.csv
    │   │   └── BOTTOM/
    │   └── ...
    └── ...
```

---

## 🎮 Guía de Uso

### Paso 1: Prepara tus Imágenes
1. Coloca tus imágenes **JPG** en la carpeta `imagenesentrada/`
2. Organiza en subcarpetas (opcional pero recomendado):
   ```
   imagenesentrada/
   ├── C1/TOP/
   ├── C1/BOTTOM/
   ├── C2/TOP/
   ├── C2/BOTTOM/
   └── ...
   ```

### Paso 2: Ejecuta el Programa
```bash
python main.py
```

### Paso 3: Visualiza los Resultados
Los resultados aparecerán en `Capturas_Procesadas/` con la misma estructura de carpetas:
- 🖼️ **Imágenes procesadas**: `resultado_[nombre].jpg`
- 📊 **Reportes CSV**: `resultados.csv` en cada carpeta

---

## 📊 Ejemplo de Salida

### Imagen Procesada
```
[Círculo verde]  ← Contorno del círculo detectado
[Manchas rojas]  ← Defectos detectados
```

### Archivo CSV (resultados.csv)
```
nombre_imagen,perimetro_circulo,perimetro_defectos,diferencia
imagen1.jpg,45.2,3.5,41.7
imagen2.jpg,48.1,5.2,42.9
imagen3.jpg,42.8,2.1,40.7
```

---

## ⚙️ Configuración Avanzada

### Archivo config.py

Edita `config.py` para ajustar parámetros:

```python
# DIMENSIONES DE PROCESAMIENTO
PROCESS_WIDTH = 1280    # Ancho de procesamiento
PROCESS_HEIGHT = 720    # Alto de procesamiento

# PARÁMETROS DE DETECCIÓN DE CÍRCULOS
params_hough = {
    'dp': 1.2,                  # Inversa del cociente de resoluciones
    'param1': 100,              # Umbral Canny superior
    'param2': 20,               # Umbral para acumular círculos
    'minRadius_factor': 0.12,   # Radio mínimo (% de imagen)
    'maxRadius_factor': 0.50    # Radio máximo (% de imagen)
}

# PARÁMETROS DE DETECCIÓN DE DEFECTOS
params = {
    'blur_kernel': 15,          # Tamaño del kernel de desenfoque
    'defect_threshold': 12,     # Umbral de defectos
    'min_defect_area': 200      # Área mínima para considerar defecto
}
```

### Consejos de Ajuste

| Parámetro | Aumentar | Disminuir |
|-----------|----------|-----------|
| `param1` | Menos círculos detectados | Más falsos positivos |
| `param2` | Círculos más precisos | Menos detecciones |
| `blur_kernel` | Menos ruido | Menos detalles |
| `defect_threshold` | Menos defectos | Más sensibilidad |

---

## 🔧 Componentes Principales

### detection/circle_detection.py
**Función: `detect_circles_hough(img)`**
- Utiliza la **Transformada de Hough** para detectar círculos
- Retorna: `(x, y, radio)` del círculo detectado
- Entrada: Imagen preprocesada
- Salida: Coordenadas del círculo

### detection/defect_detection.py
**Función: `detect_imperfections(img, x, y, r)`**
- Detecta imperfecciones dentro del área circular
- Utiliza umbrales y procesamiento morfológico
- Retorna: Lista de contornos de defectos
- Entrada: Imagen y coordenadas del círculo

### processing/image_processing.py
**Función: `process_image(path, prefix="")`**
- Pipeline completo de procesamiento
- Carga imagen → Redimensiona → Detecta círculo → Detecta defectos → Guarda resultado
- Genera estadísticas de perímetros

### processing/csv_utils.py
**Función: `save_metrics_to_csv(folder, metrics_list)`**
- Genera reportes CSV con resultados
- Incluye nombre, perímetros y diferencias
- Organiza resultados por carpeta

---

## 📈 Flujo de Procesamiento

```
┌─────────────────────────────────────┐
│   Imagen JPG (imagenesentrada/)     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  1. Redimensionar a 1280x720        │
│  2. Convertir a escala de grises    │
│  3. Aplicar Gaussiano (blur)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Detección de Círculo (Hough)       │
│  - Detecta contorno principal       │
│  - Calcula perímetro               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Detección de Defectos              │
│  - Busca imperfecciones             │
│  - Dibuja en rojo                  │
│  - Calcula perímetro total          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Almacenar Resultados               │
│  - Imagen procesada                 │
│  - Métricas en CSV                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Capturas_Procesadas/               │
│  - resultado_[nombre].jpg           │
│  - resultados.csv                   │
└─────────────────────────────────────┘
```

---

## 🎯 Ejemplo Práctico Paso a Paso

### 1. Organiza tus imágenes
```
imagenesentrada/
└── Produccion_Lote_001/
    ├── TOP/
    │   ├── pieza_001.jpg
    │   ├── pieza_002.jpg
    │   └── pieza_003.jpg
    └── BOTTOM/
        ├── pieza_001.jpg
        ├── pieza_002.jpg
        └── pieza_003.jpg
```

### 2. Ejecuta el programa
```bash
python main.py
```

### 3. Espera a que termine (verás en consola el progreso)
```
Procesando: imagenesentrada/Produccion_Lote_001/TOP/pieza_001.jpg
✓ Círculo detectado: centro=(640,360), radio=200px, perímetro=1256.64cm
✓ Defectos detectados: 3
✓ Guardado: Capturas_Procesadas/Produccion_Lote_001/TOP/resultado_pieza_001.jpg
```

### 4. Revisa los resultados
```
Capturas_Procesadas/
└── Produccion_Lote_001/
    ├── TOP/
    │   ├── resultado_pieza_001.jpg  ✓ Con círculo y defectos marcados
    │   ├── resultado_pieza_002.jpg  ✓ Con círculo y defectos marcados
    │   ├── resultado_pieza_003.jpg  ✓ Con círculo y defectos marcados
    │   └── resultados.csv          ✓ Métricas en tabla
    └── BOTTOM/
        ├── resultado_pieza_001.jpg
        ├── resultado_pieza_002.jpg
        ├── resultado_pieza_003.jpg
        └── resultados.csv
```

---

## 📝 Formato CSV Detallado

**Archivo:** `resultados.csv`

```csv
nombre_imagen,perimetro_circulo_cm,perimetro_defectos_cm,diferencia_cm,area_circulo_cm2,cantidad_defectos
pieza_001.jpg,125.66,8.5,117.16,1256.64,3
pieza_002.jpg,138.23,12.1,126.13,1520.53,5
pieza_003.jpg,113.04,5.2,107.84,1017.88,2
```

**Columnas:**
- `nombre_imagen`: Nombre del archivo procesado
- `perimetro_circulo_cm`: Perímetro del círculo detectado
- `perimetro_defectos_cm`: Perímetro total de los defectos
- `diferencia_cm`: Diferencia (círculo - defectos)
- `area_circulo_cm2`: Área del círculo
- `cantidad_defectos`: Número de defectos encontrados

---

## 🐛 Solución de Problemas

### ❌ "No se detectan círculos"
**Solución:**
1. Revisa que las imágenes tengan buena iluminación
2. Aumenta `param2` en `config.py` (menos exigente)
3. Ajusta `minRadius_factor` y `maxRadius_factor`

### ❌ "Demasiados falsos positivos"
**Solución:**
1. Disminuye `param2` en `config.py` (más exigente)
2. Reduce `blur_kernel` en `config.py`
3. Aumenta `defect_threshold`

### ❌ "Error: imagen no encontrada"
**Solución:**
1. Verifica que el archivo sea JPG
2. Comprueba la ruta en `imagenesentrada/`
3. Asegúrate de tener permisos de lectura

### ❌ "Salida sin resultados CSV"
**Solución:**
1. Verifica que hay al menos una imagen procesada correctamente
2. Revisa permisos de escritura en la carpeta destino
3. Ejecuta en la terminal para ver mensajes de error

---

## 📚 Documentación Técnica

### Algoritmos Utilizados

1. **Transformada de Hough (Círculos)**
   - Detecta formas circulares en imágenes
   - Robusto ante rotaciones y escala
   - Base: OpenCV `cv2.HoughCircles()`

2. **Thresholding Adaptativo**
   - Separa defectos del fondo
   - Funciona con diferentes iluminaciones
   - Base: `cv2.adaptiveThreshold()`

3. **Detección de Contornos**
   - Encuentra límites de defectos
   - Calcula perímetros automáticamente
   - Base: `cv2.findContours()`

---

## 📄 Licencia

Este proyecto está bajo licencia **MIT**. Eres libre de usar, modificar y distribuir este código.

---

## 👤 Autor

**David MP**  
GitHub: [@davidmp04](https://github.com/davidmp04)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -am 'Añade mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

---

## 📞 Soporte

Si tienes dudas o encuentras problemas:
1. Revisa la sección "Solución de Problemas"
2. Abre un **Issue** en GitHub
3. Consulta la documentación técnica

---

## 🎉 ¡Listo para Usar!

**Próximos pasos:**
1. ✅ Coloca tus imágenes en `imagenesentrada/`
2. ✅ Ejecuta `python main.py`
3. ✅ Revisa resultados en `Capturas_Procesadas/`
4. ✅ Analiza los reportes CSV

¡Disfruta del análisis automático de tus imágenes! 🚀
