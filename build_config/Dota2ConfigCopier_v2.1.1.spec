# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Dota 2 Config Copier v2.1.1

import os
from pathlib import Path

# Datos adicionales a incluir en el ejecutable
datas = [
    ('../config/assets/dota2.ico', '.'),  # Icono de la aplicación
    ('../config/settings.py', 'config'),  # Configuración
]

# Importaciones ocultas necesarias
hiddenimports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'pathlib',
    'json',
    'logging',
    'webbrowser',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'requests'
]

a = Analysis(
    ['../main.py'],  # Archivo principal actualizado
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'jupyter',
        'IPython'
    ],
    noarchive=False,
    optimize=2,  # Optimización máxima
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Dota2ConfigCopier_v2.1.2',  # Nombre actualizado con versión
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compresión UPX para menor tamaño
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../config/assets/dota2.ico',  # Icono del ejecutable
)
