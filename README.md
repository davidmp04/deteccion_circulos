# Detección de Círculos e Imperfecciones

Un programa Python que detecta círculos en imágenes y analiza si tienen defectos o imperfecciones dentro de ellos. Ideal para control de calidad, inspección visual automatizada o análisis de piezas circulares.

## Ramas disponibles

Este repositorio tiene dos ramas:

- **`master`**: Código limpio sin imágenes de prueba. Úsala si tienes tus propias imágenes.
- **`conimagenesdeprueba`**: Incluye ejemplos de imágenes de cada carpeta para que puedas probar el programa inmediatamente.

> ℹ️ Si quieres empezar rápido con ejemplos, clona la rama `conimagenesdeprueba`:
> ```bash
> git clone -b conimagenesdeprueba https://github.com/davidmp04/deteccion_circulos.git
> ```

## ¿Qué hace exactamente?

El programa es bastante directo en lo que hace:

1. **Detecta círculos** en tus imágenes usando visión por computadora (algoritmo HoughCircles)
2. **Identifica defectos** dentro de cada círculo (manchas, rasguños, o cualquier cosa que no sea el fondo blanco)
3. **Dibuja los resultados** con líneas de colores:
   - Línea **verde**: el círculo detectado
   - Punto **rojo**: el centro del círculo
   - Contornos **rojos**: los defectos encontrados
4. **Calcula métricas** como perímetros para análisis posterior

Luego, opcionalmente, puedes generar un archivo CSV con las mediciones de todos los círculos procesados.

## Requisitos

- Python 3.7+
- OpenCV (`cv2`)
- NumPy (`np`)

Para instalar las dependencias:

```bash
pip install opencv-python numpy
```

## Cómo usar

### Con imágenes de ejemplo (esta rama)

¡Buena noticia! Esta rama ya incluye imágenes de ejemplo en cada carpeta, así que puedes empezar directamente:

1. Ejecuta el script principal:
   ```bash
   python circulos.py
   ```

2. El programa procesará todas las imágenes de ejemplo y guardará los resultados en `Capturas_Procesadas/`

3. (Opcional) Si quieres generar un reporte CSV con las métricas:
   ```bash
   python generar_csv_mediciones.py
   ```

### Con tus propias imágenes

Si has clonado desde la rama `master` o quieres usar imágenes propias:

1. Coloca tus imágenes JPG en cualquiera de estas carpetas:
   - Carpeta raíz del proyecto
   - `Entrada/`
   - `Entrada_sincriogenia/`
   - `Salida/`
   - `Salida_sincriogenia/`

2. Ejecuta el script principal:
   ```bash
   python circulos.py
   ```

3. Los resultados se guardarán en `Capturas_Procesadas/`

### Generar reporte CSV

Después de procesar las imágenes, puedes generar un reporte:

```bash
python generar_csv_mediciones.py
```

Esto creará un archivo `Capturas_Procesadas/resultados_perimetros.csv` con:
- Nombre de la imagen
- Perímetro del círculo detectado (línea verde)
- Perímetro total de defectos (línea roja)

## Estructura del proyecto

```
.
├── circulos.py                      # Script principal de detección
├── generar_csv_mediciones.py        # Generador de reportes CSV
├── README.md                        # Documentación
├── LICENSE                          # Licencia MIT
├── Entrada/                         # Imágenes de ejemplo (rama actual)
├── Entrada_sincriogenia/            # Más imágenes de ejemplo
├── Salida/                          # Más imágenes de ejemplo
├── Salida_sincriogenia/             # Más imágenes de ejemplo
└── Capturas_Procesadas/             # Salida: aquí se guardan los resultados
```

> 📝 Nota: En la rama `master` estas carpetas no incluyen imágenes para mantener el repositorio ligero.

## Configuración

Si los resultados no son los que esperas, puedes ajustar estos parámetros en `circulos.py`:

```python
params = {
    'blur_kernel': 9,           # Cuánto desenfoque aplicar (mayor = más desenfoque)
    'draw_fraction': 0.95,      # El círculo dibujado es 95% del radio detectado
    'min_defect_area': 800,     # Área mínima para considerar algo como defecto (en píxeles)
    'defect_threshold': 25      # Sensibilidad: qué tan oscuro debe ser para considerarlo defecto
}
```

- **blur_kernel**: Si tienes mucho ruido en las imágenes, aumenta este valor. Si pierdes detalles, disminúyelo.
- **min_defect_area**: Si detecta demasiado ruido pequeño, aumenta este valor. Si se pierden defectos reales, disminúyelo.
- **defect_threshold**: Si detecta muchas cosas que no son defectos, aumenta este valor. Si no detecta defectos reales, disminúyelo.

## Archivos generados

### `circulos.py`

Módulo principal con las funciones:
- `detect_circles_hybrid(img)`: Detecta un círculo en la imagen
- `detect_imperfections(img, x, y, r)`: Encuentra defectos dentro del círculo
- `process_image(path, prefix)`: Procesa una imagen individual
- `main()`: Punto de entrada que procesa todas las imágenes disponibles

### `generar_csv_mediciones.py`

Herramienta para generar reportes. Funciones principales:
- `calcular_metricas(path)`: Analiza una imagen y extrae métricas
- `main()`: Procesa todas las imágenes y genera el CSV

## Notas técnicas

- Si tus imágenes son muy grandes (más de 1280x720), el programa las redimensiona automáticamente para acelerar el procesamiento
- El algoritmo busca solo **un círculo por imagen** (el mejor detectado)
- Los defectos se filtran por tamaño y forma para evitar falsos positivos
- Las operaciones morfológicas (abertura y cierre) limpian el ruido pequeño

## Troubleshooting

**El círculo no se detecta:**
- Asegúrate de que la imagen tiene un círculo bien definido
- Intenta ajustar los parámetros `defect_threshold` y `min_defect_area`
- Comprueba que el círculo no está demasiado cerca del borde de la imagen

**Detecta demasiados defectos falsos:**
- Aumenta `min_defect_area` para ignorar marcas muy pequeñas
- Aumenta `defect_threshold` para ser más estricto con lo que considera "defecto"

**El proceso es muy lento:**
- Las imágenes se redimensionan automáticamente si son grandes
- Si aun así es lento, los parámetros de HoughCircles se pueden ajustar para menos precisión y más velocidad

## Licencia

Este proyecto es de código abierto. Úsalo libremente.
