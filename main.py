# -*- coding: utf-8 -*-
"""
PROGRAMA PRINCIPAL - DETECCIÓN DE CÍRCULOS E IMPERFECCIONES
============================================================

Este script procesa todas las imágenes de la carpeta 'imagenesentrada/'
y genera resultados en 'Capturas_Procesadas/'.

Uso:
    python main.py

Estructura de entrada esperada:
    imagenesentrada/
    ├── C1/TOP/
    ├── C1/BOTTOM/
    ├── C2/TOP/
    ├── C2/BOTTOM/
    └── ...

Salida generada:
    Capturas_Procesadas/
    ├── C1/TOP/
    │   ├── resultado_imagen1.jpg
    │   ├── resultado_imagen2.jpg
    │   └── resultados.csv
    ├── C1/BOTTOM/
    │   ├── resultado_imagen1.jpg
    │   ├── resultado_imagen2.jpg
    │   └── resultados.csv
    └── ...
"""

import os
import sys
from pathlib import Path
import cv2
import numpy as np
from datetime import datetime

# Importar módulos del proyecto
from config import CURRENT_DIR, OUTPUT_DIR, params, params_hough
from processing.image_processing import process_image
from processing.csv_utils import init_csv, save_result


def print_header():
    """Imprime encabezado del programa."""
    print("\n" + "="*70)
    print("🔍 DETECTOR DE CÍRCULOS E IMPERFECCIONES v1.0")
    print("="*70)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Carpeta entrada: {CURRENT_DIR}")
    print(f"Carpeta salida: {OUTPUT_DIR}")
    print("="*70 + "\n")


def print_footer(total, exitosas, fallidas):
    """Imprime resumen final."""
    print("\n" + "="*70)
    print("📊 RESUMEN DE PROCESAMIENTO")
    print("="*70)
    print(f"Total de imágenes procesadas: {total}")
    print(f"✓ Exitosas: {exitosas}")
    print(f"✗ Fallidas: {fallidas}")
    print(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")


def find_image_folders(base_dir):
    """
    Encuentra todas las carpetas que contienen imágenes JPG.
    
    Args:
        base_dir: Directorio base para buscar
        
    Returns:
        Lista de tuplas (carpeta, ruta_relativa)
    """
    folders = []
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"⚠️  Advertencia: La carpeta {base_dir} no existe")
        print(f"   Creando carpeta: {base_dir}")
        base_path.mkdir(parents=True, exist_ok=True)
        return folders
    
    # Buscar todas las subcarpetas
    for folder in base_path.rglob("*"):
        if folder.is_dir():
            # Verificar si hay imágenes JPG en esta carpeta
            jpg_files = list(folder.glob("*.jpg")) + list(folder.glob("*.JPG"))
            if jpg_files:
                relative_path = folder.relative_to(base_path)
                folders.append((folder, str(relative_path)))
    
    return sorted(folders)


def process_images_in_folder(folder_path, relative_path):
    """
    Procesa todas las imágenes JPG en una carpeta.
    
    Args:
        folder_path: Ruta completa de la carpeta
        relative_path: Ruta relativa para organizar salida
        
    Returns:
        Tupla (exitosas, fallidas)
    """
    exitosas = 0
    fallidas = 0
    
    print(f"\n📁 Procesando: {relative_path}")
    print("-" * 70)
    
    # Obtener todas las imágenes JPG
    jpg_files = sorted(
        list(folder_path.glob("*.jpg")) + 
        list(folder_path.glob("*.JPG"))
    )
    
    if not jpg_files:
        print(f"   ℹ️  No hay imágenes JPG en esta carpeta")
        return 0, 0
    
    # Inicializar CSV para esta carpeta
    init_csv(relative_path)
    
    # Procesar cada imagen
    for jpg_file in jpg_files:
        try:
            print(f"   ⏳ Procesando: {jpg_file.name}...", end=" ")
            
            # Procesar imagen y obtener métricas
            result_path, metrics = process_image(str(jpg_file), prefix=relative_path)
            
            if result_path and metrics:
                # Guardar resultado en CSV
                save_result(relative_path, metrics)
                print("✓ OK")
                exitosas += 1
            else:
                print("✗ Error en detección")
                fallidas += 1
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            fallidas += 1
    
    print("-" * 70)
    print(f"   Resumen: {exitosas} exitosas, {fallidas} fallidas")
    
    return exitosas, fallidas


def main():
    """Función principal."""
    
    # Mostrar encabezado
    print_header()
    
    # Verificar configuración
    print("⚙️  Configuración Actual:")
    print(f"   - Dimensiones: {1280}x{720}")
    print(f"   - Parámetros Hough: dp={params_hough['dp']}, param1={params_hough['param1']}, param2={params_hough['param2']}")
    print(f"   - Parámetros Defectos: blur_kernel={params['blur_kernel']}, threshold={params['defect_threshold']}")
    print()
    
    # Buscar carpetas con imágenes
    print("🔎 Buscando carpetas con imágenes...")
    folders = find_image_folders(CURRENT_DIR)
    
    if not folders:
        print("❌ No se encontraron carpetas con imágenes JPG")
        print(f"   Coloca imágenes en: {CURRENT_DIR}")
        print(f"   Ejemplo: {CURRENT_DIR}/C1/TOP/imagen.jpg")
        return
    
    print(f"✓ Se encontraron {len(folders)} carpetas con imágenes\n")
    
    # Procesar todas las carpetas
    total_exitosas = 0
    total_fallidas = 0
    
    for folder_path, relative_path in folders:
        exitosas, fallidas = process_images_in_folder(folder_path, relative_path)
        total_exitosas += exitosas
        total_fallidas += fallidas
    
    # Mostrar resumen final
    print_footer(
        total_exitosas + total_fallidas,
        total_exitosas,
        total_fallidas
    )
    
    # Información de salida
    if total_exitosas > 0:
        print("📂 Resultados disponibles en:")
        print(f"   {OUTPUT_DIR}")
        print("\n✅ ¡Procesamiento completado!")
    else:
        print("⚠️  No se procesaron imágenes correctamente")
        print("   Revisa las configuraciones en config.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Procesamiento interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
