# -*- coding: utf-8 -*-
"""
MÓDULO DE DETECCIÓN DE CÍRCULOS

Detecta círculos dentro de las imágenes usando un sistema híbrido.

Mejoras aplicadas:
- Uso de Canny antes de Hough para mejorar estabilidad
- Rango de radios ajustado para evitar detectar agujeros interiores
- Dibujo del círculo ligeramente ampliado para coincidir con el borde real
"""

import cv2
import numpy as np

from config import params, params_hough, PROCESS_WIDTH, PROCESS_HEIGHT


# ---------------------------------------------------
# DETECCIÓN HÍBRIDA DE CÍRCULOS
# ---------------------------------------------------

def detect_circles_hybrid(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur_size = params['blur_kernel']
    if blur_size % 2 == 0:
        blur_size += 1

    blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)

    # NUEVO: detectar bordes
    edges = cv2.Canny(blurred, 50, 150)

    result = img.copy()
    detected = []

    h, w = gray.shape[:2]
    center_x, center_y = w / 2, h / 2

    # ---------------------------------------------------
    # MÉTODO 1 - CANNY + HOUGH
    # ---------------------------------------------------

    circles = cv2.HoughCircles(
        edges,
        cv2.HOUGH_GRADIENT,
        dp=params_hough['dp'],
        minDist=params_hough['param1'],
        param1=params_hough['param1'],
        param2=params_hough['param2'],
        minRadius=int(min(w, h) * 0.30),
        maxRadius=int(min(w, h) * 0.60)
    )

    if circles is not None and len(circles[0]) > 0:

        valid_circles = []

        for c in circles[0]:

            x, y, r = c

            dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

            if dist < min(w, h) * 0.55:
                valid_circles.append((x, y, r, dist))

        if valid_circles:

            valid_circles.sort(key=lambda x: x[3])

            x, y, r, _ = valid_circles[0]

            x, y, r = int(x), int(y), int(r)

            detected.append((x, y, r))

            # dibujar ligeramente más grande
            r_draw = int(r * 1.03)

            cv2.circle(result, (x, y), r_draw, (0, 255, 0), 24)
            cv2.circle(result, (x, y), 8, (0, 0, 255), -1)

            print(f"[MÉTODO 1 - Canny+Hough] Círculo detectado: centro=({x}, {y}), radio={r}")

            return result, detected

    # ---------------------------------------------------
    # MÉTODO 2 - HOUGH TRADICIONAL
    # ---------------------------------------------------

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=2,
        minDist=max(w // 2, h // 2),
        param1=50,
        param2=20,
        minRadius=int(min(w, h) * 0.30),
        maxRadius=int(min(w, h) * 0.65)
    )

    if circles is not None:

        x, y, r = circles[0][0]

        x, y, r = int(x), int(y), int(r)

        detected.append((x, y, r))

        r_draw = int(r * 1.03)

        cv2.circle(result, (x, y), r_draw, (0, 255, 0), 24)
        cv2.circle(result, (x, y), 8, (0, 0, 255), -1)

        print(f"[MÉTODO 2 - Hough Tradicional] Círculo detectado: centro=({x}, {y}), radio={r}")

        return result, detected

    print("[SIN DETECCIÓN] No se pudo detectar el círculo")

    return result, detected


# ---------------------------------------------------
# REDUCCIÓN PARA DETECCIÓN RÁPIDA
# ---------------------------------------------------

def _resize_for_detection(img):

    h, w = img.shape[:2]

    if w <= PROCESS_WIDTH and h <= PROCESS_HEIGHT:
        return img, 1.0

    scale = min(PROCESS_WIDTH / w, PROCESS_HEIGHT / h)

    new_w = int(round(w * scale))
    new_h = int(round(h * scale))

    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    return resized, scale


# ---------------------------------------------------
# DETECCIÓN RÁPIDA
# ---------------------------------------------------

def detect_circles_fast(orig):

    small, scale = _resize_for_detection(orig)

    result_small, circles_small = detect_circles_hybrid(small)

    if circles_small:

        inv = 1.0 / scale

        x, y, r = circles_small[0]

        x = int(round(x * inv))
        y = int(round(y * inv))
        r = int(round(r * inv))

        result = orig.copy()

        r_draw = int(r * 1.03)

        cv2.circle(result, (x, y), r_draw, (0, 255, 0), 24)
        cv2.circle(result, (x, y), 8, (0, 0, 255), -1)

        return result, [(x, y, r)]

    return detect_circles_hybrid(orig)