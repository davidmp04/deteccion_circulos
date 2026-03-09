# -*- coding: utf-8 -*-
"""
DETECCIÓN DE IMPERFECCIONES

Este módulo detecta defectos dentro del círculo identificado.

El proceso es:
1. Crear máscara circular
2. Calcular diferencia respecto al brillo máximo
3. Binarizar
4. Eliminar ruido con morfología
5. Analizar contornos
"""

import cv2
import numpy as np

from config import params


def detect_imperfections(img, x, y, r):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mask = np.zeros_like(gray)

    cv2.circle(mask, (x, y), int(r * 0.85), 255, -1)

    circle_region = cv2.bitwise_and(gray, gray, mask=mask)

    diff = 255 - circle_region

    _, thresh = cv2.threshold(
        diff,
        params['defect_threshold'],
        255,
        cv2.THRESH_BINARY
    )

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

            if circularity > 0.8:
                continue

            defects.append(c)

    return defects