# -*- coding: utf-8 -*-
"""
DETECCIÓN DE IMPERFECCIONES

Detecta defectos dentro del círculo identificado.

Mejoras:
- Detecta defectos claros y oscuros
- Funciona con fondo claro o fondo oscuro
- Mejora contraste
"""

import cv2
import numpy as np

from config import params


def detect_imperfections(img, x, y, r):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # mejorar contraste
    gray = cv2.equalizeHist(gray)

    # máscara del círculo
    mask = np.zeros_like(gray)
    cv2.circle(mask, (x, y), int(r * 0.95), 255, -1)

    circle = cv2.bitwise_and(gray, gray, mask=mask)

    # ------------------------------------------------
    # DETECCIÓN DE IMPERFECCIONES CLARAS
    # ------------------------------------------------

    blur = cv2.GaussianBlur(circle, (21, 21), 0)

    diff_light = cv2.subtract(circle, blur)

    _, thresh_light = cv2.threshold(
        diff_light,
        params['defect_threshold'],
        255,
        cv2.THRESH_BINARY
    )

    # ------------------------------------------------
    # DETECCIÓN DE IMPERFECCIONES OSCURAS
    # ------------------------------------------------

    diff_dark = cv2.subtract(blur, circle)

    _, thresh_dark = cv2.threshold(
        diff_dark,
        params['defect_threshold'],
        255,
        cv2.THRESH_BINARY
    )

    # ------------------------------------------------
    # COMBINAR RESULTADOS
    # ------------------------------------------------

    thresh = cv2.bitwise_or(thresh_light, thresh_dark)

    thresh = cv2.bitwise_and(thresh, thresh, mask=mask)

    kernel = np.ones((5, 5), np.uint8)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    defects = []

    for c in contours:

        area = cv2.contourArea(c)

        if area > params['min_defect_area']:

            perimeter = cv2.arcLength(c, True)

            if perimeter == 0:
                continue

            circularity = 4 * np.pi * area / (perimeter * perimeter)

            # eliminar manchas muy circulares
            if circularity > 0.85:
                continue

            defects.append(c)

    return defects