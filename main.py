# -*- coding: utf-8 -*-
"""
PROGRAMA PRINCIPAL

Busca todas las imágenes .jpg en las carpetas:

- raíz
- Entrada
- Entrada_sincriogenia
- Salida
- Salida_sincriogenia

y procesa cada una.
"""

import os
from pathlib import Path

from config import CURRENT_DIR, OUTPUT_DIR
from processing.image_processing import process_image


def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    dirs = [
        CURRENT_DIR,
        CURRENT_DIR / 'Entrada',
        CURRENT_DIR / 'Entrada_sincriogenia',
        CURRENT_DIR / 'Salida',
        CURRENT_DIR / 'Salida_sincriogenia',
        CURRENT_DIR / 'TOP',
        CURRENT_DIR / 'BOTOM',
        # rutas explícitas para las subcarpetas dentro de 'nuevas'
        CURRENT_DIR / 'nuevas',
        CURRENT_DIR / 'nuevas' / 'C1',
        CURRENT_DIR / 'nuevas' / 'C1' / 'BOTOM',
        CURRENT_DIR / 'nuevas' / 'C1' / 'TOP',
        CURRENT_DIR / 'nuevas' / 'C2_Fondo opaco_exposicion_sports_',
        CURRENT_DIR / 'nuevas' / 'C2_Fondo opaco_exposicion_sports_' / 'BOTOM',
        CURRENT_DIR / 'nuevas' / 'C2_Fondo opaco_exposicion_sports_' / 'TOP',
        CURRENT_DIR / 'nuevas' / 'C3_opaco_expo_auto_',
        CURRENT_DIR / 'nuevas' / 'C3_opaco_expo_auto_' / 'BOTOM',
        CURRENT_DIR / 'nuevas' / 'C3_opaco_expo_auto_' / 'TOP',
        CURRENT_DIR / 'nuevas' / 'C4_resolucionyparametros',
        CURRENT_DIR / 'nuevas' / 'C4_resolucionyparametros' / 'BOTOM',
        CURRENT_DIR / 'nuevas' / 'C4_resolucionyparametros' / 'TOP',
        CURRENT_DIR / 'nuevas' / 'c5_sinfilamentoled',
        CURRENT_DIR / 'nuevas' / 'c5_sinfilamentoled' / 'BOTOM',
        CURRENT_DIR / 'nuevas' / 'c5_sinfilamentoled' / 'TOP',
        CURRENT_DIR / 'nuevas' / 'C6_primeraresoluciony nuevosparametros',
        CURRENT_DIR / 'nuevas' / 'C6_primeraresoluciony nuevosparametros' / 'BOTOM',
        CURRENT_DIR / 'nuevas' / 'C6_primeraresoluciony nuevosparametros' / 'TOP',
        CURRENT_DIR / 'nuevas' / 'C7_definitiva',
        CURRENT_DIR / 'nuevas' / 'C7_definitiva' / 'BOTOM',
        CURRENT_DIR / 'nuevas' / 'C7_definitiva' / 'TOP',
        CURRENT_DIR / 'nuevas' / 'C3_definitiva',
        CURRENT_DIR / 'nuevas' / 'C3_definitiva' / 'BOTTOM',
        CURRENT_DIR / 'nuevas' / 'C3_definitiva' / 'TOP',
        CURRENT_DIR / 'nuevas' / 'CAPTURA DEFINITIVA 1' / 'BOTTOM',
        CURRENT_DIR / 'nuevas' / 'CAPTURA DEFINITIVA 1' / 'TOP',
    ]

    seen = set()

    files_with_prefix = []

    for d in dirs:

        if not d.exists():
            continue

        prefix = str(d.relative_to(CURRENT_DIR)).replace(os.sep, '/')

        for f in list(d.glob('*.JPG')) + list(d.glob('*.jpg')):

            key = (str(f.resolve()), prefix)

            if key in seen:
                continue

            seen.add(key)

            files_with_prefix.append((f, prefix))

    files_with_prefix.sort(key=lambda x: x[0].name.lower())

    if not files_with_prefix:

        print("❌ No se encontraron imágenes")

        return

    print(f"Se encontraron {len(files_with_prefix)} imagenes")

    print("=" * 60)

    for i, (img_path, prefix) in enumerate(files_with_prefix):

        print(f"\n[{i+1}/{len(files_with_prefix)}] Siguiente: {img_path.name} ({prefix})", flush=True)

        process_image(str(img_path), prefix)

    print("\n" + "=" * 60)

    print("Procesamiento completado!")


if __name__ == "__main__":
    main()