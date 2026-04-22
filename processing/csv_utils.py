# -*- coding: utf-8 -*-

import os
import csv
from pathlib import Path
from config import OUTPUT_DIR


def init_csv(subdir=""):

    output_dir = OUTPUT_DIR / subdir if subdir else OUTPUT_DIR

    os.makedirs(output_dir, exist_ok=True)

    csv_file = output_dir / "resultados.csv"

    if not csv_file.exists():

        with open(csv_file, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                "nombre_imagen",
                "perimetro_circulo",
                "perimetro_imperfecciones",
                "diferencia"
            ])


def save_result(nombre, perimetro_circulo, perimetro_defectos, subdir=""):

    output_dir = OUTPUT_DIR / subdir if subdir else OUTPUT_DIR

    csv_file = output_dir / "resultados.csv"

    diferencia = perimetro_circulo - perimetro_defectos

    with open(csv_file, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            nombre,
            round(perimetro_circulo, 2),
            round(perimetro_defectos, 2),
            round(diferencia, 2)
        ])