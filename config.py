# -*- coding: utf-8 -*-
"""
CONFIGURACIÓN GLOBAL DEL PROGRAMA

Este archivo centraliza todos los parámetros del sistema para que
puedan modificarse fácilmente sin tocar el resto del código.

Incluye:
- Dimensiones de procesamiento
- Directorios del proyecto
- Parámetros de detección de círculos
- Parámetros de detección de imperfecciones
"""

import os
from pathlib import Path

# ---------------------------------------------------
# DIMENSIONES DE PROCESAMIENTO
# ---------------------------------------------------

PROCESS_WIDTH = 1280
PROCESS_HEIGHT = 720

# ---------------------------------------------------
# DIRECTORIOS
# ---------------------------------------------------

CURRENT_DIR = Path(__file__).parent / "imagenesentrada"
OUTPUT_DIR = CURRENT_DIR.parent / "Capturas_Procesadas"

# ---------------------------------------------------
# PARÁMETROS AJUSTABLES
# ---------------------------------------------------

params = {
    'blur_kernel': 15,
    'draw_fraction': 0.95,
    'min_defect_area': 200,
    'defect_threshold': 12,
    'canny_low': 50,
    'canny_high': 150
}

params_hough = {
    'dp': 1.2,
    'param1': 100,
    'param2': 20,
    'minRadius_factor': 0.12,
    'maxRadius_factor': 0.50
}