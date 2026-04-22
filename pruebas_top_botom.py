# -*- coding: utf-8 -*-
"""
PRUEBAS UNITARIAS PARA TOP Y BOTOM

Script simple para probar la detección básica en TOP y BOTOM.
"""

import csv
import os
import cv2
import numpy as np
from pathlib import Path
from config import CURRENT_DIR, OUTPUT_DIR
from detection.circle_detection import detect_circles_fast
from detection.defect_detection import detect_imperfections
from processing.utils import save_images, imshow


def test_circle_detection(image_path):
    """Prueba unitaria: detectar círculos y defectos, mostrar defectos dibujados en rojo."""
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"❌ No se pudo cargar {image_path}")
        return None

    result, circles = detect_circles_fast(img)

    if circles:
        print(f"✅ Círculo detectado en {Path(image_path).name}")
        
        x, y, r = circles[0]
        
        # Detectar imperfecciones
        defects = detect_imperfections(result, x, y, r)
        print(f"   Imperfecciones detectadas: {len(defects)}")
        
        # Dibujar los defectos detectados en ROJO
        for defect in defects:
            cv2.drawContours(result, [defect], -1, (0, 0, 255), 3)
        
        return result
    else:
        print(f"❌ No se detectó círculo en {Path(image_path).name}")
        return None


def test_basic_processing(folder_name):
    """Prueba unitaria básica: procesar todas las imágenes de una carpeta."""
    folder_path = CURRENT_DIR / folder_name
    if not folder_path.exists():
        print(f"❌ Carpeta {folder_name} no existe")
        return

    images = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.png"))
    print(f"📁 Procesando {len(images)} imágenes en {folder_name}")

    for img_path in images[:3]:  # Solo primeras 3 para prueba rápida
        result = test_circle_detection(img_path)
        if result is not None:
            # Mostrar resultado
            imshow(f"Resultado {folder_name}", result)

            # Guardar
            base_name = f"test_{Path(img_path).stem}"
            save_images(result, base_name, "")


if __name__ == "__main__":
    print("🚀 Iniciando pruebas unitarias TOP/BOTOM")

    # Prueba TOP
    test_basic_processing("TOP")

    # Prueba BOTOM
    test_basic_processing("BOTOM")

    print("✅ Pruebas completadas")
