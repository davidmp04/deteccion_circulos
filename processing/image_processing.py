# -*- coding: utf-8 -*-
"""
PROCESAMIENTO DE IMÁGENES CON CÍRCULO VERDE E IMPERFECCIONES ROJAS
"""

import cv2
import numpy as np
from pathlib import Path

from detection.defect_detection import detect_imperfections
from processing.utils import save_images, imshow
from processing.csv_utils import init_csv, save_result

# ==============================================
# DETECCIÓN DE CÍRCULOS AJUSTADA
# ==============================================
def detect_circles_fast(img):
    """
    Detecta un círculo principal en la imagen usando HoughCircles,
    filtrando por radio y proximidad al centro.
    Devuelve el resultado limpio y la lista de círculos.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    h, w = gray.shape
    cx, cy = w // 2, h // 2

    expected_r = 485  # Radio aproximado
    min_r, max_r = 470, 500

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=h // 2,
        param1=100,
        param2=30,
        minRadius=min_r,
        maxRadius=max_r
    )

    if circles is not None:
        circles = np.uint16(np.around(circles[0, :]))
        # Filtrar por radio más cercano al esperado
        circles = sorted(circles, key=lambda c: abs(c[2] - expected_r))
        # Filtrar por proximidad al centro
        circles = sorted(circles, key=lambda c: (c[0] - cx) ** 2 + (c[1] - cy) ** 2)
        x, y, r = circles[0]
        return img.copy(), [(x, y, r)]
    else:
        return img.copy(), []

# ==============================================
# PROCESAMIENTO DE UNA IMAGEN
# ==============================================
def process_image(path, prefix=""):
    try:
        init_csv(prefix)
        orig = cv2.imread(path)

        if orig is None:
            print(f"❌ Error: no se pudo cargar {path}", flush=True)
            return

        # Detectar círculo (mejorado)
        result, circles = detect_circles_fast(orig)

        print(f"\nProcesando {Path(path).name} ({prefix or 'raíz'})", flush=True)

        perimetro_defectos = 0

        if circles:
            x, y, r = circles[0]

            # Dibujar el círculo detectado en VERDE
            cv2.circle(result, (x, y), r, (0, 255, 0), 5)

            # Detectar imperfecciones dentro del círculo usando tu sistema
            defects = detect_imperfections(orig, x, y, r)
            print(f"   Imperfecciones detectadas: {len(defects)}")

            # Dibujar las imperfecciones en ROJO
            for defect in defects:
                cv2.drawContours(result, [defect], -1, (0, 0, 255), 15)
                perimetro_defectos += cv2.arcLength(defect, True)

        base = Path(path).stem

        extra = ""
        if circles:
            perim_circulo = 2 * np.pi * r
            perim_cm = int(round(perim_circulo))
            extra = f"{perim_cm}cm"
            save_result(base, perim_circulo, perimetro_defectos, prefix)

        imshow('Resultado', result)
        save_images(result, base, extra, prefix)

    except Exception as e:
        print(f"❌ Error procesando {path}: {e}", flush=True)