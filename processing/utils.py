# -*- coding: utf-8 -*-
"""
UTILIDADES DEL PROGRAMA

Funciones auxiliares para:
- Mostrar imágenes
- Guardar resultados
"""

import os
import cv2

from config import OUTPUT_DIR


def save_images(cam_img, base_name, extra=""):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if extra:
        basename = f"resultado_{base_name}_{extra}.jpg"
    else:
        basename = f"resultado_{base_name}.jpg"

    cam_path = os.path.join(OUTPUT_DIR, basename)

    cv2.imwrite(cam_path, cam_img)

    print(f"   guardado: {cam_path}", flush=True)


def imshow(title, img):

    cv2.imshow(title, img)
    cv2.waitKey(1)