# -*- coding: utf-8 -*-
"""
PROCESAMIENTO DE IMÁGENES

Este módulo coordina el procesamiento completo de cada imagen:

1. Cargar imagen
2. Detectar círculo
3. Detectar imperfecciones
4. Dibujar resultados
5. Guardar imagen procesada
"""

import cv2
import numpy as np
from pathlib import Path

from detection.circle_detection import detect_circles_fast
from detection.defect_detection import detect_imperfections
from processing.utils import save_images, imshow


def process_image(path, prefix=""):

    try:

        orig = cv2.imread(path)

        if orig is None:
            print(f"❌ Error: no se pudo cargar {path}", flush=True)
            return

        result, circles = detect_circles_fast(orig)

        print(f"\nProcesando {Path(path).name} ({prefix or 'raíz'})", flush=True)

        if circles:

            x, y, r = circles[0]

            defects = detect_imperfections(result, x, y, r)

            print(f"   Imperfecciones detectadas: {len(defects)}")

            for defect in defects:
                cv2.drawContours(result, [defect], -1, (0, 0, 255), 15)

        base = Path(path).stem

        if prefix:
            base = f"{prefix}_{base}"

        extra = ""

        if circles:

            perim = 2 * np.pi * r
            perim_cm = int(round(perim))

            extra = f"{perim_cm}cm"

        imshow('Resultado', result)

        save_images(result, base, extra)

    except Exception as e:

        print(f"❌ Error procesando {path}: {e}", flush=True)