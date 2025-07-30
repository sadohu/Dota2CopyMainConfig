# -*- mode: python ; coding: utf-8 -*-
"""
DotaTwin v3.1.0 Portable Build Specification
Este spec crea la versión portable de DotaTwin incluyendo Python embebido
"""

import os
import shutil
from pathlib import Path

# Configuración de la versión
APP_VERSION = "3.1.0"
APP_NAME = "DotaTwin"
PYTHON_EMBEDDED_URL = "https://www.python.org/ftp/python/3.12.8/python-3.12.8-embed-amd64.zip"

def create_portable_build():
    """
    Crea la distribución portable de DotaTwin
    """
    print(f"🚀 Creando {APP_NAME} v{APP_VERSION} Portable...")
    
    # Directorios
    base_dir = Path(".")
    dist_dir = base_dir / "dist"
    portable_dir = dist_dir / "portable"
    src_dir = base_dir / "src"
    config_dir = base_dir / "config"
    
    # Limpiar directorio portable si existe
    if portable_dir.exists():
        print("🧹 Limpiando directorio portable existente...")
        shutil.rmtree(portable_dir)
    
    # Crear estructura portable
    print("📁 Creando estructura de directorios...")
    portable_dir.mkdir(parents=True, exist_ok=True)
    (portable_dir / "src").mkdir(exist_ok=True)
    (portable_dir / "python").mkdir(exist_ok=True)
    
    # Copiar código fuente
    print("📋 Copiando código fuente...")
    
    # Lista de archivos y directorios a copiar
    source_items = [
        ("main.py", "src/main.py"),
        ("src", "src/src"),
        ("config", "src/config"),
    ]
    
    for src_path, dst_path in source_items:
        src_full = base_dir / src_path
        dst_full = portable_dir / dst_path
        
        if src_full.exists():
            if src_full.is_dir():
                shutil.copytree(src_full, dst_full, dirs_exist_ok=True)
            else:
                dst_full.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_full, dst_full)
            print(f"  ✓ {src_path} -> {dst_path}")
    
    # Crear launcher
    print("🚀 Creando launcher...")
    launcher_content = '''#!/usr/bin/env python3
"""
DotaTwin Portable Launcher
Configura el entorno y ejecuta DotaTwin desde el código fuente
"""

import sys
import os
from pathlib import Path

def main():
    # Configurar el directorio base
    base_dir = Path(__file__).parent
    
    # Agregar el directorio src al path para importar módulos
    src_dir = base_dir / "src"
    if src_dir.exists():
        sys.path.insert(0, str(src_dir))
        sys.path.insert(0, str(base_dir))
    
    print("DotaTwin v3.1.0 Portable")
    print("========================")
    
    # Verificar tkinter
    try:
        import tkinter
        print("✓ tkinter disponible")
    except ImportError:
        print("⚠ Warning: tkinter no está disponible")
        print("  La aplicación GUI puede no funcionar.")
        print("  Asegúrate de usar Python con tkinter.")
        input("Presiona Enter para continuar...")
        return
    
    # Verificar Pillow (opcional)
    try:
        from PIL import Image
        print("✓ Pillow disponible")
    except ImportError:
        print("⚠ Warning: Pillow no está disponible")
        print("  Algunas funciones de imagen pueden no funcionar.")
    
    print("\\nIniciando DotaTwin...")
    
    # Intentar ejecutar DotaTwin
    try:
        # Importar desde el directorio src
        sys.path.insert(0, str(src_dir))
        from main import main as app_main
        app_main()
        
    except Exception as e:
        print(f"Error al ejecutar DotaTwin: {e}")
        print("\\nDetalles del error:")
        import traceback
        traceback.print_exc()
        input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()'''
    
    with open(portable_dir / "DotaTwin_launcher.py", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    # Crear batch file
    print("⚡ Creando run.bat...")
    batch_content = '''@echo off
title DotaTwin v3.1.0 Portable
cd /d "%~dp0"

echo.
echo ======================================
echo  DotaTwin v3.1.0 Portable
echo  Twin your Dota experience
echo ======================================
echo.

REM Verificar que Python embebido está disponible
if not exist "python\\python.exe" (
    echo ERROR: No se encontró Python embebido en la carpeta python\\
    echo Verifica que hayas extraído correctamente el archivo portable.
    pause
    exit /b 1
)

REM Ejecutar DotaTwin
echo Iniciando DotaTwin...
python\\python.exe DotaTwin_launcher.py

REM Verificar si hubo error
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo ejecutar DotaTwin
    echo Verifica que todos los archivos estén presentes.
    pause
)'''
    
    with open(portable_dir / "run.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    # Crear requirements.txt
    print("📦 Creando requirements.txt...")
    requirements_content = '''# DotaTwin v3.1.0 Requirements
# Solo se requiere para funcionalidades opcionales

# Para mejor manejo de imágenes (opcional)
Pillow>=8.0.0

# Incluido en Python estándar:
# - tkinter (GUI)
# - json (configuraciones)
# - pathlib (manejo de rutas)
# - logging (sistema de logs)
# - subprocess (ejecución de comandos)'''
    
    with open(portable_dir / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    
    # Crear instrucciones
    print("📖 Creando instrucciones...")
    instructions = '''======================================
   DotaTwin v3.1.0 Portable
======================================

VERSIÓN PORTABLE SIN INSTALACIÓN
================================

Esta es la versión portable de DotaTwin que no requiere instalación y evita las alertas de Windows SmartScreen.

INSTRUCCIONES DE USO:
====================

OPCIÓN 1 - Ejecutar con run.bat (Recomendado):
----------------------------------------------
1. Doble click en "run.bat"
2. Si aparece alerta de tkinter, ver soluciones abajo

OPCIÓN 2 - Usar Python del sistema:
-----------------------------------
Si tienes Python instalado en tu sistema:
1. Ejecutar: python DotaTwin_launcher.py
2. O: python src\\main.py

SOLUCIÓN PARA PROBLEMA DE TKINTER:
==================================

Si ves el error "tkinter no está disponible":

MÉTODO 1 - Usar Python del sistema (Recomendado):
- Instala Python desde python.org (incluye tkinter)
- Ejecuta: python DotaTwin_launcher.py

MÉTODO 2 - Usar ejecutable PyInstaller:
- Descarga DotaTwin_v3.1.0.exe desde GitHub Releases
- Acepta la alerta de Windows SmartScreen (es seguro)

CONTACTO Y SOPORTE:
==================
- GitHub: https://github.com/sadohu/DotaTwin
- Issues: Reporta problemas en GitHub Issues

====================================
        ¡Disfruta DotaTwin!
===================================='''
    
    with open(portable_dir / "INSTRUCCIONES_PORTABLE.txt", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print(f"✅ {APP_NAME} v{APP_VERSION} Portable creado exitosamente!")
    print(f"📁 Ubicación: {portable_dir}")
    print("🔄 Para descargar Python embebido, ejecuta: python build_portable.py --download-python")
    print("📦 Para crear ZIP final, ejecuta: python build_portable.py --create-zip")

def download_python_embedded():
    """
    Descarga Python embebido para el portable
    """
    import urllib.request
    import zipfile
    
    print("⬇️ Descargando Python 3.12 embebido...")
    
    portable_dir = Path("dist/portable")
    python_dir = portable_dir / "python"
    
    # Crear directorio si no existe
    python_dir.mkdir(parents=True, exist_ok=True)
    
    # Descargar Python embebido
    zip_path = python_dir / "python-embed.zip"
    
    try:
        urllib.request.urlretrieve(PYTHON_EMBEDDED_URL, zip_path)
        print("✅ Python embebido descargado")
        
        # Extraer
        print("📦 Extrayendo Python embebido...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(python_dir)
        
        # Eliminar ZIP
        zip_path.unlink()
        print("✅ Python embebido configurado")
        
    except Exception as e:
        print(f"❌ Error descargando Python: {e}")
        print("💡 Descarga manualmente desde: " + PYTHON_EMBEDDED_URL)

def create_zip():
    """
    Crea el ZIP final del portable
    """
    import zipfile
    
    print("📦 Creando ZIP portable...")
    
    portable_dir = Path("dist/portable")
    zip_path = Path(f"dist/{APP_NAME}_v{APP_VERSION}_Portable.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in portable_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(portable_dir)
                zipf.write(file_path, arcname)
    
    # Obtener tamaño
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    
    print(f"✅ ZIP creado: {zip_path}")
    print(f"📏 Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    import sys
    
    if "--download-python" in sys.argv:
        download_python_embedded()
    elif "--create-zip" in sys.argv:
        create_zip()
    else:
        create_portable_build()
        
        # Preguntar si desea descargar Python
        response = input("\\n¿Descargar Python embebido ahora? (y/n): ")
        if response.lower() in ['y', 'yes', 's', 'si']:
            download_python_embedded()
            
            # Preguntar si desea crear ZIP
            response = input("\\n¿Crear ZIP portable ahora? (y/n): ")
            if response.lower() in ['y', 'yes', 's', 'si']:
                create_zip()
