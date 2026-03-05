# -*- coding: utf-8 -*-
"""
Detección de Círculos e Imperfecciones en Imágenes

Este módulo permite detectar círculos en imágenes y analizar si tienen defectos
o imperfecciones dentro de ellos. Usa algoritmos de visión por computadora
(OpenCV) para identificar estos patrones.

Las imágenes se cargan desde varias carpetas de entrada y los resultados
(imágenes procesadas con anotaciones) se guardan en la carpeta 'Capturas_Procesadas'.
"""

import os
import time
import cv2
import numpy as np
from pathlib import Path

try:    
    from google.colab.patches import cv2_imshow
except ImportError:
    cv2_imshow = None


def imshow(title, img):
    # En modo headless (sin pantalla) no mostramos las imágenes,
    # solo las guardamos como archivos. Útil para servidores sin GUI.
    pass


# Configuración de procesamiento
PROCESS_WIDTH = 1280
PROCESS_HEIGHT = 720
OUTPUT_DIR = "Capturas_Procesadas"
CURRENT_DIR = Path(__file__).parent

# Parámetros ajustables para la detección
# Si los círculos no se detectan bien o detecta cosas que no quieres,
# aquí es donde se modifican estos valores
params = {
    'blur_kernel': 9,           # Cuánto "desenfoqué" la imagen (menos ruido)
    'draw_fraction': 0.95,      # El círculo dibujado es 95% del radio detectado
    'min_defect_area': 800,     # Área mínima para considerar algo como un defecto
    'defect_threshold': 25      # Sensibilidad para detectar diferencias de brillo
}




# ---------------------------------------------------
# DETECCIÓN DE CÍRCULOS
# ---------------------------------------------------
def detect_circles_hybrid(img):
    """
    Detecta círculos en una imagen usando el algoritmo HoughCircles.
    
    Si la imagen es muy grande (más de 1280x720), la redimensiona primero
    para acelerar el procesamiento. El círculo detectado se escala de vuelta
    a las coordenadas de la imagen original.
    
    Args:
        img: Imagen en formato BGR (como lee OpenCV)
        
    Returns:
        (imagen_resultado, lista_circulos): 
        - imagen_resultado tiene el círculo dibujado en verde
        - lista_circulos contiene tuplas (x, y, radio) del círculo detectado
    """
    print("     [1] Comenzando detección...", flush=True)
    
    orig_h, orig_w = img.shape[:2]
    scale = 1.0
    
    # Si la imagen es muy grande, redimensionarla para más rapidez
    if orig_w > 1280 or orig_h > 720:
        scale = min(1280 / orig_w, 720 / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        img_proc = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        print(f"     [2] Redimensionada: {orig_w}x{orig_h} -> {new_w}x{new_h}", flush=True)
    else:
        img_proc = img.copy()
        print(f"     [2] Sin redimensionar: {orig_w}x{orig_h}", flush=True)

    # Convertir a escala de grises y desenfocar para reducir ruido
    gray = cv2.cvtColor(img_proc, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    print("     [3] Preprocesamiento completado", flush=True)

    result = img_proc.copy()
    detected = []
    h, w = gray.shape[:2]

    # HoughCircles es el algoritmo que detecta los círculos
    print("     [4] Ejecutando HoughCircles...", flush=True)
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=2,              # Razón de acumulador
        minDist=w // 3,    # Distancia mínima entre círculos
        param1=50,         # Umbral de detección de bordes
        param2=20,         # Umbral de acumulador
        minRadius=int(min(w, h) * 0.15),   # Radio mínimo a buscar
        maxRadius=int(min(w, h) * 0.40)    # Radio máximo a buscar
    )
    print("     [5] HoughCircles completó", flush=True)

    if circles is not None:
        # Tomamos el primer círculo detectado (el mejor match)
        first_circle = circles[0][0]
        x = int(first_circle[0])
        y = int(first_circle[1])
        r = int(first_circle[2])
        
        # Escalar de vuelta a las coordenadas originales si redimensionamos
        if scale < 1.0:
            x = int(x / scale)
            y = int(y / scale)
            r = int(r / scale)
        
        detected.append((x, y, r))
        
        r_draw = max(int(r * params['draw_fraction']), 1)
        if scale < 1.0:
            # Dibujar en la imagen redimensionada para mostrar
            cv2.circle(img_proc, (int(first_circle[0]), int(first_circle[1])), int(first_circle[2] * params['draw_fraction']), (0, 255, 0), 6)
        else:
            cv2.circle(result, (x, y), r_draw, (0, 255, 0), 6)
        
        print(f"[HOUGH] círculo detectado r={r}", flush=True)
        return result, detected
    
    print(f"[HOUGH] NO DETECTADO", flush=True)
    return result, detected


# ---------------------------------------------------
# DETECCIÓN DE IMPERFECCIONES Y DEFECTOS
# ---------------------------------------------------
def detect_imperfections(img, x, y, r):
    """
    Encuentra imperfecciones (defectos) dentro de un círculo.
    
    El algoritmo busca áreas que sean significativamente más oscuras que
    el fondo (diferencia de brillo mayor al threshold). Luego filtra ruido
    y contornos que sean demasiado circulares (son más bien manchas naturales).
    
    Args:
        img: Imagen en formato BGR
        x, y: Coordenadas del centro del círculo
        r: Radio del círculo
        
    Returns:
        Lista de contornos que representan los defectos encontrados
    """
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Crear una máscara circular para aislar solo el área dentro del círculo
    mask = np.zeros_like(gray)
    cv2.circle(mask, (x, y), int(r * 0.9), 255, -1)

    # Extraer solo la región dentro del círculo
    circle_region = cv2.bitwise_and(gray, gray, mask=mask)

    # Calcular la diferencia respecto al máximo brillo (255)
    # Las áreas oscuras tendrán valores altos
    diff = 255 - circle_region

    # Binarizar: solo valores por encima del threshold se mantienen
    _, thresh = cv2.threshold(
        diff,
        params['defect_threshold'],
        255,
        cv2.THRESH_BINARY
    )

    # Aplicar máscara de nuevo para eliminar lo que salga del círculo
    thresh = cv2.bitwise_and(thresh, thresh, mask=mask)

    # Limpiar ruido pequeño con operaciones morfológicas
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)   # Elimina ruido
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  # Cierra huecos

    # Encontrar los contornos de lo que quedó
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    defects = []

    for c in contours:
        area = cv2.contourArea(c)

        # Ignorar contornos demasiado pequeños
        if area > params['min_defect_area']:

            perimeter = cv2.arcLength(c, True)

            if perimeter == 0:
                continue

            # Calcular circularidad. Circles cercanos a 1, formas irregulares cercanas a 0
            circularity = 4 * np.pi * area / (perimeter * perimeter)

            # Ignorar si es demasiado circular (probablemente no es un defecto real)
            if circularity > 0.75:
                continue

            defects.append(c)

    return defects


# ---------------------------------------------------
# UTILIDADES DE PROCESAMIENTO
# ---------------------------------------------------
def save_images(cam_img, base_name, extra=""):
    """
    Guarda una imagen procesada en la carpeta de salida.
    
    Args:
        cam_img: La imagen a guardar
        base_name: Nombre base del archivo
        extra: Información adicional para añadir al nombre (ej: perímetro)
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if extra:
        basename = f"resultado_{base_name}_{extra}.jpg"
    else:
        basename = f"resultado_{base_name}.jpg"

    cam_path = os.path.join(OUTPUT_DIR, basename)
    cv2.imwrite(cam_path, cam_img)
    print(f"   guardado: {cam_path}", flush=True)


def process_image(path, prefix=""):
    """
    Procesa una imagen individual: detecta círculos, imperfecciones
    y guarda el resultado con anotaciones.
    
    Args:
        path: Ruta a la imagen
        prefix: Prefijo para indicar de dónde viene la imagen
    """
    try:
        orig = cv2.imread(path)
        if orig is None:
            print(f"❌ Error: no se pudo cargar {path}", flush=True)
            return

        result, circles = detect_circles_hybrid(orig)

        print(f"\nProcesando {Path(path).name} ({prefix or 'raíz'})", flush=True)
        
        if circles:
            print(f"   DEBUG: Detectado r={circles[0][2]}", flush=True)
            print(f"   [P1] Extrayendo coordenadas...", flush=True)

            x, y, r = circles[0]
            r_draw = max(int(r * params['draw_fraction']), 1)
            print(f"   [P2] Dibujando círculo...", flush=True)

            # Dibujar el círculo detectado (verde) y su centro (rojo) en la imagen original
            cv2.circle(orig, (x, y), r_draw, (0, 255, 0), 10)   # Círculo: verde
            cv2.circle(orig, (x, y), 8, (0, 0, 255), -1)        # Centro: rojo
            print(f"   [P3] Círculo dibujado, detectando imperfecciones...", flush=True)

            # Buscar defectos únicamente dentro del círculo
            defects = detect_imperfections(orig, x, y, r)
            print(f"   [P4] Imperfecciones detectadas: {len(defects)}", flush=True)

            # Dibujar los defectos en rojo
            for defect in defects:
                cv2.drawContours(orig, [defect], -1, (0, 0, 255), 4)
            print(f"   [P5] Imperfecciones dibujadas", flush=True)

        print(f"   [P6] Preparando para guardar...", flush=True)
        base = Path(path).stem
        if prefix:
            base = f"{prefix}_{base}"

        extra = ""
        if circles:
            # Calcular perímetro del círculo detectado
            perim = 2 * np.pi * r
            perim_cm = int(round(perim))
            extra = f"{perim_cm}cm"
        
        print(f"   [P7] Mostrando/guardando...", flush=True)
        imshow('Resultado', orig)
        save_images(orig, base, extra)
        print(f"   [P8] Completado", flush=True)
    except Exception as e:
        print(f"❌ Error procesando {path}: {e}", flush=True)


# ---------------------------------------------------
# FUNCIÓN PRINCIPAL
# ---------------------------------------------------
def main():
    """
    Punto de entrada del programa. 
    
    Busca todas las imágenes .jpg en las carpetas de entrada,
    las procesa una por una, y guarda los resultados en 'Capturas_Procesadas'.
    
    Buscará en estas carpetas:
    - Raíz del proyecto
    - Entrada
    - Entrada_sincriogenia
    - Salida
    - Salida_sincriogenia
    """
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Directorios donde buscamos las imágenes
    dirs = [
        CURRENT_DIR,
        CURRENT_DIR / 'Entrada',
        CURRENT_DIR / 'Entrada_sincriogenia',
        CURRENT_DIR / 'Salida',
        CURRENT_DIR / 'Salida_sincriogenia',
    ]
    seen = set()
    files_with_prefix = []

    # Recolectar todas las imágenes
    for d in dirs:
        if not d.exists():
            continue
        prefix = '' if d == CURRENT_DIR else d.name

        for f in list(d.glob('*.JPG')) + list(d.glob('*.jpg')):
            key = (str(f.resolve()), prefix)
            if key in seen:
                continue
            seen.add(key)
            files_with_prefix.append((f, prefix))

    files_with_prefix.sort(key=lambda x: x[0].name.lower())

    if not files_with_prefix:
        print("❌ No se encontraron imágenes")
        return

    print(f"Se encontraron {len(files_with_prefix)} imagenes")
    print("=" * 60)

    # Procesar cada imagen
    for i, (img_path, prefix) in enumerate(files_with_prefix):
        print(f"\n[{i+1}/{len(files_with_prefix)}] Siguiente: {img_path.name} ({prefix})", flush=True)
        process_image(str(img_path), prefix)

    print("\n" + "=" * 60)
    print("Procesamiento completado!")


if __name__ == "__main__":
    main()