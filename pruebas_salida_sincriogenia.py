# -*- coding: utf-8 -*-
"""
PRUEBAS UNITARIAS PARA SALIDA_SINCRIOGENIA
Versión específica para probar detección de imperfecciones en imágenes de Salida_sincriogenia
"""

import os
import cv2
import numpy as np
from pathlib import Path

# ---------------------------------------------------
# CONFIGURACIÓN GLOBAL
# ---------------------------------------------------

# Dimensiones de procesamiento
PROCESS_WIDTH = 1280
PROCESS_HEIGHT = 720

# Directorios
CURRENT_DIR = Path(__file__).parent
OUTPUT_DIR = CURRENT_DIR / "Capturas_Procesadas"

# ===== PARÁMETROS AJUSTABLES =====
# Parámetros optimizados para detección de imperfecciones
params = {
    'blur_kernel': 15,          # Más blur como en el código del profesor
    'draw_fraction': 0.95,
    'min_defect_area': 50,      # Reducido para detectar imperfecciones más pequeñas
    'max_defect_area': 500000,  # Área máxima (no se usa mucho aquí)
    'defect_threshold': 6,      # Umbral para el método de diferencia
    'min_perimeter': 20,        # Perímetro mínimo para detectar imperfecciones
    'aspect_ratio': 1.2,        # Reducido de 2.0 para detectar líneas menos alargadas
    'canny_low': 50,            # Umbral bajo para Canny
    'canny_high': 150           # Umbral alto para Canny
}

# Parámetros mejorados basados en el código del profesor
params_hough = {
    'dp': 1.2,                  # Como el profesor
    'param1': 100,              # Como el profesor
    'param2': 25,               # Bajado para más detecciones
    'minRadius_factor': 0.12,
    'maxRadius_factor': 0.50
}
# ================================

# ---------------------------------------------------
# FUNCIONES DE DETECCIÓN
# ---------------------------------------------------

def detect_circles_hybrid(img):
    """
    Detecta círculos usando método híbrido mejorado.
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur más fuerte como en el código del profesor
    blur_size = params['blur_kernel']
    if blur_size % 2 == 0:
        blur_size += 1
    blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)

    result = img.copy()
    detected = []
    h, w = gray.shape[:2]
    center_x, center_y = w / 2, h / 2

    # --- MÉTODO 1: HoughCircles con Canny ---
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=params_hough['dp'],
        minDist=params_hough['param1'],
        param1=params_hough['param1'],
        param2=params_hough['param2'],
        minRadius=int(min(w, h) * params_hough['minRadius_factor']),
        maxRadius=int(min(w, h) * params_hough['maxRadius_factor'])
    )

    if circles is not None and len(circles[0]) > 0:
        valid_circles = []
        for c in circles[0]:
            x, y, r = c[0], c[1], c[2]
            dist_to_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            if dist_to_center < min(w, h) * 0.45:
                valid_circles.append((x, y, r, dist_to_center))

        if valid_circles:
            valid_circles.sort(key=lambda x: x[3])
            x, y, r, _ = valid_circles[0]
            x, y, r = int(x), int(y), int(r)
            detected.append((x, y, r))

            r_draw = max(int(r * params['draw_fraction']), 1)
            cv2.circle(result, (x, y), r_draw, (0, 255, 0), 24)
            cv2.circle(result, (x, y), 8, (0, 0, 255), -1)
            print(f"[CÍRCULO DETECTADO] centro=({x}, {y}), radio={r}")
            return result, detected

    # --- MÉTODO 2: HoughCircles tradicional ---
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=2,
        minDist=max(w // 2, h // 2),
        param1=50,
        param2=20,
        minRadius=int(min(w, h) * 0.12),
        maxRadius=int(min(w, h) * 0.50)
    )

    if circles is not None and len(circles[0]) > 0:
        valid_circles = []
        for c in circles[0]:
            x, y, r = c[0], c[1], c[2]
            dist_to_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            if dist_to_center < min(w, h) * 0.45:
                valid_circles.append((x, y, r, dist_to_center))

        if valid_circles:
            valid_circles.sort(key=lambda x: x[3])
            x, y, r, _ = valid_circles[0]
            x, y, r = int(x), int(y), int(r)
            detected.append((x, y, r))

            r_draw = max(int(r * params['draw_fraction']), 1)
            cv2.circle(result, (x, y), r_draw, (0, 255, 0), 24)
            cv2.circle(result, (x, y), 8, (0, 0, 255), -1)
            print(f"[CÍRCULO DETECTADO] centro=({x}, {y}), radio={r}")
            return result, detected

    # --- MÉTODO 3: HoughCircles más flexible ---
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.5,
        minDist=max(w // 3, h // 3),
        param1=40,
        param2=18,
        minRadius=int(min(w, h) * 0.10),
        maxRadius=int(min(w, h) * 0.55)
    )

    if circles is not None and len(circles[0]) > 0:
        valid_circles = []
        for c in circles[0]:
            x, y, r = c[0], c[1], c[2]
            dist_to_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            if dist_to_center < min(w, h) * 0.45:
                valid_circles.append((x, y, r, dist_to_center))

        if valid_circles:
            valid_circles.sort(key=lambda x: x[3])
            x, y, r, _ = valid_circles[0]
            x, y, r = int(x), int(y), int(r)
            detected.append((x, y, r))

            r_draw = max(int(r * params['draw_fraction']), 1)
            cv2.circle(result, (x, y), r_draw, (0, 255, 0), 24)
            cv2.circle(result, (x, y), 8, (0, 0, 255), -1)
            print(f"[CÍRCULO DETECTADO] centro=({x}, {y}), radio={r}")
            return result, detected

    # --- MÉTODO 4: Threshold + Contours ---
    _, thresh = cv2.threshold(
        blurred, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
        valid_contours = []
        for c in contours:
            area = cv2.contourArea(c)
            if area > 10000:
                (x, y), r = cv2.minEnclosingCircle(c)
                dist_to_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                if r > 0 and r < min(w, h) * 0.6 and dist_to_center < min(w, h) * 0.45:
                    valid_contours.append((x, y, r, dist_to_center))

        if valid_contours:
            valid_contours.sort(key=lambda x: x[3])
            x, y, r, _ = valid_contours[0]
            x, y, r = int(x), int(y), int(r)
            detected.append((x, y, r))

            r_draw = max(int(r * params['draw_fraction']), 1)
            cv2.circle(result, (x, y), r_draw, (0, 255, 0), 24)
            print(f"[CÍRCULO DETECTADO] centro=({x}, {y}), radio={r}")
            return result, detected

    print(f"[SIN DETECCIÓN] No se pudo detectar el círculo")
    return result, detected


def detect_imperfections(img, x, y, r):
    """
    Detecta imperfecciones dentro del círculo.
    Estrategia: conectar píxeles rojos cercanos en componentes grandes
    y reportar solo las lascas/grietas significativas.
    """

    # Crear máscara circular
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    mask_radius = int(r * 0.95)
    cv2.circle(mask, (x, y), mask_radius, 255, -1)

    # Extraer región dentro del círculo
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    # Detectar píxeles rojos
    b, g, r_channel = cv2.split(masked_img)
    red_mask = (r_channel > 120) & (g < 120) & (b < 120)
    
    print(f"   DEBUG: Píxeles rojos detectados inicialmente: {red_mask.sum()}")

    if red_mask.sum() < 50:
        print(f"   DEBUG: Insuficientes píxeles rojos")
        return []

    # Crear imagen binaria de píxeles rojos
    red_binary = np.zeros_like(b)
    red_binary[red_mask] = 255

    # MORFOLIGIA AGRESIVA: Dilatación grande para conectar píxeles cercanos
    # en grupos significativos (lascas)
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    red_binary = cv2.dilate(red_binary, kernel_dilate, iterations=2)
    
    # Erosión para recuperar tamaño aproximado pero mantener conexiones
    kernel_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    red_binary = cv2.erode(red_binary, kernel_erode, iterations=1)

    cv2.imshow('DEBUG_red_mask', red_binary)
    cv2.waitKey(1)

    # Encontrar contornos de las componentes conectadas grandes
    contours, _ = cv2.findContours(
        red_binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    print(f"   DEBUG: {len(contours)} contornos tras morfología")
    defects = []

    for c in contours:
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)
        x0, y0, w0, h0 = cv2.boundingRect(c)

        print(f"      Contorno: area={area:.1f}, perim={perimeter:.1f}, w={w0}, h={h0}")

        # Filtros para detectar imperfecciones (lascas):
        # - Área mínima mayor para evitar puntos pequeños (>500)
        # - Área máxima para evitar el círculo completo (<50,000)
        if 500 < area < 50000:
            defects.append(c)
            print("         -> ACEPTADO (lasca grande)")
        else:
            print("         -> ignorado (área fuera de rango)")

    print(f"   DEBUG: Imperfecciones finales: {len(defects)}")
    return defects
# ---------------------------------------------------

def _resize_for_detection(img):
    """Devuelve (imagen_redimensionada, factor_escala) para detect."""
    h, w = img.shape[:2]
    if w <= PROCESS_WIDTH and h <= PROCESS_HEIGHT:
        return img, 1.0
    scale_w = PROCESS_WIDTH / w
    scale_h = PROCESS_HEIGHT / h
    scale = min(scale_w, scale_h)
    new_w = int(round(w * scale))
    new_h = int(round(h * scale))
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized, scale


def detect_circles_fast(orig):
    """Intenta detectar el círculo en una versión reducida para ganar velocidad."""
    small, scale = _resize_for_detection(orig)
    result_small, circles_small = detect_circles_hybrid(small)
    if circles_small:
        inv = 1.0 / scale
        x, y, r = circles_small[0]
        x = int(round(x * inv))
        y = int(round(y * inv))
        r = int(round(r * inv))
        r_draw = max(int(r * params['draw_fraction']), 1)
        result = orig.copy()
        cv2.circle(result, (x, y), r_draw, (0, 255, 0), 24)
        cv2.circle(result, (x, y), 8, (0, 0, 255), -1)
        return result, [(x, y, r)]
    return detect_circles_hybrid(orig)


def save_images(cam_img, base_name, extra=""):
    """
    Guarda una imagen procesada en la carpeta de salida.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if extra:
        basename = f"{base_name}_{extra}.jpg"
    else:
        basename = f"{base_name}.jpg"

    cam_path = os.path.join(OUTPUT_DIR, basename)
    cv2.imwrite(cam_path, cam_img)
    print(f"   guardado: {cam_path}", flush=True)


def imshow(title, img):
    """Muestra una imagen en una ventana."""
    cv2.imshow(title, img)
    cv2.waitKey(1)


# ---------------------------------------------------
# PROCESAMIENTO DE IMÁGENES
# ---------------------------------------------------

def process_image(path, prefix=""):
    """
    Procesa una imagen individual: detecta círculos, imperfecciones
    y guarda el resultado con anotaciones.
    """
    try:
        orig = cv2.imread(path)
        if orig is None:
            print(f"❌ Error: no se pudo cargar {path}", flush=True)
            return

        result, circles = detect_circles_fast(orig)

        print(f"\nProcesando {Path(path).name} ({prefix or 'Salida_sincriogenia'})", flush=True)

        if circles:
            print(f"   DEBUG: Detectado r={circles[0][2]}", flush=True)
            x, y, r = circles[0]
            print(f"   Detectando imperfecciones en círculo centro=({x},{y}), radio={r}...", flush=True)

            defects = detect_imperfections(result, x, y, r)
            print(f"   DEBUG: Función detect_imperfections retornó {len(defects)} defectos", flush=True)

            if defects:
                print(f"   Imperfecciones detectadas: {len(defects)}", flush=True)
                # Dibujar los defectos en rojo
                for defect in defects:
                    cv2.drawContours(result, [defect], -1, (0, 0, 255), 15)
                print(f"   Imperfecciones dibujadas en rojo", flush=True)
            else:
                print(f"   AVISO: No se detectaron imperfecciones en esta imagen", flush=True)

        orig = result

        base = Path(path).stem
        if prefix:
            base = f"{prefix}_{base}"

        extra = ""
        if circles:
            perim = 2 * np.pi * r
            perim_cm = int(round(perim))
            extra = f"{perim_cm}cm"

        imshow('Resultado Prueba', orig)
        save_images(orig, base, extra)
        print(f"   Completado", flush=True)
    except Exception as e:
        print(f"❌ Error procesando {path}: {e}", flush=True)


# ---------------------------------------------------
# FUNCIÓN PRINCIPAL
# ---------------------------------------------------
def main():
    """
    Punto de entrada del programa de pruebas unitarias.
    Solo procesa imágenes de la carpeta Salida_sincriogenia.
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Solo buscar en Salida_sincriogenia
    dir_sincriogenia = CURRENT_DIR / 'Salida_sincriogenia'
    if not dir_sincriogenia.exists():
        print("❌ La carpeta Salida_sincriogenia no existe")
        return

    files_with_prefix = []
    prefix = 'Salida_sincriogenia'

    for f in list(dir_sincriogenia.glob('*.JPG')) + list(dir_sincriogenia.glob('*.jpg')):
        files_with_prefix.append((f, prefix))

    files_with_prefix.sort(key=lambda x: x[0].name.lower())

    if not files_with_prefix:
        print("❌ No se encontraron imágenes en Salida_sincriogenia")
        return

    print(f"Se encontraron {len(files_with_prefix)} imágenes en Salida_sincriogenia")
    print("=" * 60)

    # Procesar cada imagen
    for i, (img_path, prefix) in enumerate(files_with_prefix):
        print(f"\n[{i+1}/{len(files_with_prefix)}] Procesando: {img_path.name}", flush=True)
        process_image(str(img_path), prefix)

    print("\n" + "=" * 60)
    print("Pruebas unitarias completadas!")


if __name__ == "__main__":
    main()