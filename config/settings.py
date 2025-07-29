"""
Configuración centralizada de la aplicación Dota 2 Config Copier.

Este módulo contiene todas las configuraciones y constantes de la aplicación,
siguiendo el principio de separación de responsabilidades.
"""

import os
from pathlib import Path
from typing import Dict, Any

# ═══════════════════════════════════════════════════════════════════════════
# INFORMACIÓN DE LA APLICACIÓN
# ═══════════════════════════════════════════════════════════════════════════

APP_NAME = "Dota 2 Config Copier"
APP_VERSION = "2.1.1"
VERSION = APP_VERSION  # Alias para compatibilidad
APP_AUTHOR = "Sadohu"
APP_DESCRIPTION = "Aplicación para copiar configuraciones de Dota 2 entre cuentas de Steam"

# ═══════════════════════════════════════════════════════════════════════════
# RUTAS DEL SISTEMA
# ═══════════════════════════════════════════════════════════════════════════

# Rutas base del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIG_DIR = PROJECT_ROOT / "config"
DOCS_DIR = PROJECT_ROOT / "docs"

# Rutas de Steam (Windows)
STEAM_USERDATA_PATH = Path(r"C:\Program Files (x86)\Steam\userdata")
AVATAR_CACHE_PATH = Path(r"C:\Program Files (x86)\Steam\config\avatarcache")

# Archivos de configuración
CACHE_FILE = "ultima_seleccion.json"
ICON_PATH = "dota2.ico"
LOG_FILE = "app.log"

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIONES DE LA INTERFAZ
# ═══════════════════════════════════════════════════════════════════════════

# Configuraciones de paginación
DEFAULT_ITEMS_PER_PAGE = 10
ITEMS_PER_PAGE = DEFAULT_ITEMS_PER_PAGE  # Alias para compatibilidad
MIN_ITEMS_PER_PAGE = 5
MAX_ITEMS_PER_PAGE = 50
ITEMS_PER_PAGE_OPTIONS = [10, 15, 20, 25, 30]

# Dimensiones de la ventana
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT_WIDTH = 1000
WINDOW_DEFAULT_HEIGHT = 700

# Configuraciones de imagen
AVATAR_SIZE = (32, 32)
DEFAULT_AVATAR_COLOR = (64, 64, 64)

# ═══════════════════════════════════════════════════════════════════════════
# ESTILOS Y COLORES
# ═══════════════════════════════════════════════════════════════════════════

# Colores para estados de cuenta
COLORS = {
    "origen": "#d0f0ff",      # Azul claro
    "destino": "#e0ffe0",     # Verde claro
    "normal": "#f0f0f0",      # Gris claro
    "ignorada": "#ffcccc",    # Rojo claro
    "selected_page": "lightblue"
}

# Iconos Unicode para la interfaz
ICONS = {
    # Botones principales
    "origen": "📤",
    "destino": "📥",
    "ignorar": "🚫",
    "restaurar": "↩️",
    "copiar": "📋",
    "cancelar": "❌",
    
    # Navegación
    "anterior": "⬅️",
    "siguiente": "➡️",
    
    # Títulos e información
    "cuentas": "🎮",
    "ignoradas": "🔕",
    "pagina": "📄",
    "configuracion": "⚙️",
    "info": "ℹ️",
    "warning": "⚠️",
    "error": "❌",
    "success": "✅"
}

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIONES DE JUEGO
# ═══════════════════════════════════════════════════════════════════════════

# ID de Dota 2 en Steam
DOTA2_APP_ID = "570"

# Patrones de archivos a copiar
CONFIG_PATTERNS = [
    "*.cfg",
    "*.vdf",
    "*.dat",
    "*.txt"
]

# Carpetas a excluir durante la copia
EXCLUDE_FOLDERS = [
    "temp",
    "cache",
    "logs"
]

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIONES DE LOGGING
# ═══════════════════════════════════════════════════════════════════════════

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "formatter": "detailed"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIONES POR DEFECTO
# ═══════════════════════════════════════════════════════════════════════════

DEFAULT_CONFIG = {
    "origen": "",
    "destino": "",
    "cuentas_ignoradas": [],
    "items_por_pagina": DEFAULT_ITEMS_PER_PAGE,
    "window_geometry": f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}",
    "auto_backup": True,
    "show_confirmations": True
}

# ═══════════════════════════════════════════════════════════════════════════
# MENSAJES DE LA APLICACIÓN
# ═══════════════════════════════════════════════════════════════════════════

MESSAGES = {
    "confirm_ignore": "¿Deseas ignorar la cuenta '{}'?\n\nPodrás restaurarla desde la pestaña 'Cuentas Ignoradas'.",
    "confirm_copy": "¿Deseas copiar la configuración de:\n\n{} → {} ?",
    "success_copy": "La configuración fue copiada con éxito.",
    "error_same_account": "Origen y destino no pueden ser iguales.",
    "select_accounts": "Selecciona origen y destino",
    "ready_to_copy": "Listo para copiar de '{}' a '{}'",
    "no_accounts": "No se encontraron cuentas de Steam con Dota 2",
    "no_ignored_accounts": "No hay cuentas ignoradas",
    "error_steam_path": "No se encontró la instalación de Steam en la ruta estándar",
    "error_permissions": "Error de permisos. Ejecuta como administrador.",
    "error_copy_failed": "Error copiando archivos: {}"
}

def get_config_value(key: str, default: Any = None) -> Any:
    """
    Obtiene un valor de configuración.
    
    Args:
        key: Clave de configuración
        default: Valor por defecto si no existe la clave
        
    Returns:
        Valor de configuración
    """
    return DEFAULT_CONFIG.get(key, default)

def validate_steam_paths() -> bool:
    """
    Valida que las rutas de Steam existan.
    
    Returns:
        True si las rutas son válidas
    """
    return STEAM_USERDATA_PATH.exists() and AVATAR_CACHE_PATH.exists()
