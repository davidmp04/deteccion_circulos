# -*- coding: utf-8 -*-
"""
Generador de Reportes CSV de Mediciones

Toma las imágenes procesadas de la carpeta 'Capturas_Procesadas' y genera
un archivo CSV con métricas sobre los círculos y sus defectos.

Para cada imagen genera:
- Perímetro del círculo detectado (línea verde)
- Perímetro total de todos los defectos encontrados (línea roja)

Esto es útil para análisis posterior o para generar reportes.
"""

import csv
import cv2
import numpy as np
from pathlib import Path

# Importamos las funciones de detección del módulo principal
from circulos import detect_circles_hybrid, detect_imperfections

# Rutas de trabajo
CARPETA_PROCESADAS = Path(__file__).parent / "Capturas_Procesadas"
OUTPUT_CSV = CARPETA_PROCESADAS / "resultados_perimetros.csv"


def calcular_metricas(path):
    """
    Analiza una imagen y calcula métricas de perímetros.
    
    Para cada imagen, detecta el círculo y sus defectos,
    luego calcula el perímetro total de ambos.
    
    Args:
        path: Ruta a un archivo de imagen
        
    Returns:
        Tupla (perímetro_círculo, perímetro_defectos) o None si hay error
    """
    
    img = cv2.imread(str(path))
    if img is None:
        return None

    # Detectar el círculo en la imagen
    result, circles = detect_circles_hybrid(img)

    if not circles:
        return None

    # Extraer la posición y radio del círculo
    x, y, r = circles[0]

    # Calcular el perímetro del círculo (línea verde)
    perimetro_verde = 2 * np.pi * r

    # Buscar imperfecciones dentro del círculo
    defects = detect_imperfections(img, x, y, r)

    # Sumar el perímetro de todas las imperfecciones (línea roja)
    perimetro_rojo_total = 0
    for defect in defects:
        perimetro_rojo_total += cv2.arcLength(defect, True)

    return perimetro_verde, perimetro_rojo_total


def main():
    """
    Función principal que genera el CSV.
    
    Lee todas las imágenes de Capturas_Procesadas, calcula las métricas
    y las guarda en un archivo CSV.
    """
    
    # Verificar que existe la carpeta de entrada
    if not CARPETA_PROCESADAS.exists():
        print("❌ No existe la carpeta Capturas_Procesadas")
        return

    filas = []

    # Procesar cada imagen JPG en la carpeta
    for img_path in CARPETA_PROCESADAS.glob("*.jpg"):

        metricas = calcular_metricas(img_path)

        if metricas is None:
            continue

        per_verde, per_rojo = metricas

        # Añadir una fila al resultado
        filas.append([
            img_path.name,
            round(per_verde, 2),
            round(per_rojo, 2)
        ])

    # Escribir el archivo CSV
    with open(OUTPUT_CSV, mode="w", newline="") as f:
        writer = csv.writer(f)
        # Encabezados
        writer.writerow([
            "imagen",
            "perimetro_linea_verde",
            "perimetro_linea_roja"
        ])
        # Datos
        writer.writerows(filas)

    print("✅ CSV generado en:", OUTPUT_CSV)


if __name__ == "__main__":
    main()