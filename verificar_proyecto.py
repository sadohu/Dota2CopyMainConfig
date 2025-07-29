#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación del estado del proyecto Dota 2 Config Copier v2.0

Este script valida que toda la arquitectura modular esté funcionando correctamente:
- Importación de módulos
- Servicios principales
- Componentes UI
- Tests automatizados
- Configuración
"""

import sys
import os
from pathlib import Path
import importlib
import subprocess
from typing import Dict, List, Tuple, Any

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_header(title: str) -> None:
    """Imprime un header formateado"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{title.center(60)}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}\n")

def print_status(item: str, status: bool, details: str = "") -> None:
    """Imprime el estado de un item"""
    status_symbol = f"{Colors.GREEN}✓{Colors.RESET}" if status else f"{Colors.RED}✗{Colors.RESET}"
    print(f"{status_symbol} {item}")
    if details:
        print(f"  {Colors.YELLOW}└─ {details}{Colors.RESET}")

def verificar_estructura_archivos() -> Tuple[bool, List[str]]:
    """Verifica que todos los archivos necesarios existan"""
    archivos_requeridos = [
        'main.py',
        'config/settings.py',
        'config/__init__.py',
        'src/__init__.py',
        'src/models/__init__.py',
        'src/models/domain_models.py',
        'src/core/__init__.py',
        'src/core/steam_service.py',
        'src/core/config_service.py',
        'src/gui/__init__.py',
        'src/gui/main_app.py',
        'src/gui/main_tab.py',
        'src/gui/ignored_tab.py',
        'src/utils/__init__.py',
        'src/utils/logging_utils.py',
        'src/utils/ui_utils.py',
        'tests/__init__.py',
        'tests/test_refactor.py',
        'requirements.txt',
        'README.md',
        'CHANGELOG.md',
        'ARQUITECTURA_MODULAR.md',
        'MIGRACION_V2.md'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not Path(archivo).exists():
            archivos_faltantes.append(archivo)
    
    return len(archivos_faltantes) == 0, archivos_faltantes

def verificar_importaciones() -> Tuple[bool, List[str]]:
    """Verifica que todos los módulos se puedan importar correctamente"""
    modulos_principales = [
        'config.settings',
        'src.models.domain_models',
        'src.core.steam_service',
        'src.core.config_service',
        'src.gui.main_app',
        'src.gui.main_tab',
        'src.gui.ignored_tab',
        'src.utils.logging_utils',
        'src.utils.ui_utils'
    ]
    
    errores_importacion = []
    for modulo in modulos_principales:
        try:
            importlib.import_module(modulo)
        except Exception as e:
            errores_importacion.append(f"{modulo}: {str(e)}")
    
    return len(errores_importacion) == 0, errores_importacion

def verificar_clases_principales() -> Tuple[bool, List[str]]:
    """Verifica que las clases principales estén disponibles"""
    verificaciones = []
    
    try:
        from src.models.domain_models import SteamAccount, PaginationInfo, AppConfig
        verificaciones.append("Domain Models: ✓")
    except Exception as e:
        verificaciones.append(f"Domain Models: ✗ ({e})")
    
    try:
        from src.core.steam_service import SteamAccountService, AccountFilterService
        verificaciones.append("Steam Services: ✓")
    except Exception as e:
        verificaciones.append(f"Steam Services: ✗ ({e})")
    
    try:
        from src.core.config_service import ConfigurationService, FileCopyService
        verificaciones.append("Config Services: ✓")
    except Exception as e:
        verificaciones.append(f"Config Services: ✗ ({e})")
    
    try:
        from src.gui.main_app import Dota2ConfigCopierApp
        verificaciones.append("Main App: ✓")
    except Exception as e:
        verificaciones.append(f"Main App: ✗ ({e})")
    
    try:
        from src.utils.logging_utils import LoggingMixin
        from src.utils.ui_utils import AvatarManager
        verificaciones.append("Utilities: ✓")
    except Exception as e:
        verificaciones.append(f"Utilities: ✗ ({e})")
    
    errores = [v for v in verificaciones if "✗" in v]
    return len(errores) == 0, verificaciones

def ejecutar_tests() -> Tuple[bool, str]:
    """Ejecuta los tests automatizados"""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'tests.test_refactor'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        success = result.returncode == 0
        output = result.stdout + result.stderr
        
        return success, output
    except subprocess.TimeoutExpired:
        return False, "Tests ejecutados por más de 30 segundos (timeout)"
    except Exception as e:
        return False, f"Error ejecutando tests: {str(e)}"

def verificar_configuracion() -> Tuple[bool, str]:
    """Verifica que la configuración esté correcta"""
    try:
        from config.settings import APP_NAME, VERSION, ITEMS_PER_PAGE
        
        if not APP_NAME or not VERSION:
            return False, "Configuración básica incompleta"
        
        if ITEMS_PER_PAGE <= 0:
            return False, "Configuración de paginación inválida"
        
        return True, f"Configuración OK: {APP_NAME} v{VERSION}"
    except Exception as e:
        return False, f"Error en configuración: {str(e)}"

def main():
    """Función principal de verificación"""
    print_header("VERIFICACIÓN DEL PROYECTO DOTA 2 CONFIG COPIER v2.0")
    
    # Verificar estructura de archivos
    print(f"{Colors.BOLD}1. Verificando estructura de archivos...{Colors.RESET}")
    archivos_ok, archivos_faltantes = verificar_estructura_archivos()
    print_status("Estructura de archivos", archivos_ok, 
                 f"{len(archivos_faltantes)} archivos faltantes" if archivos_faltantes else "Todos los archivos presentes")
    
    if archivos_faltantes:
        print(f"  {Colors.RED}Archivos faltantes:{Colors.RESET}")
        for archivo in archivos_faltantes:
            print(f"    - {archivo}")
    
    # Verificar importaciones
    print(f"\n{Colors.BOLD}2. Verificando importaciones de módulos...{Colors.RESET}")
    importaciones_ok, errores_importacion = verificar_importaciones()
    print_status("Importaciones de módulos", importaciones_ok,
                 f"{len(errores_importacion)} errores" if errores_importacion else "Todos los módulos se importan correctamente")
    
    if errores_importacion:
        print(f"  {Colors.RED}Errores de importación:{Colors.RESET}")
        for error in errores_importacion:
            print(f"    - {error}")
    
    # Verificar clases principales
    print(f"\n{Colors.BOLD}3. Verificando clases principales...{Colors.RESET}")
    clases_ok, verificaciones_clases = verificar_clases_principales()
    print_status("Clases principales", clases_ok, "Todas las clases están disponibles" if clases_ok else "Algunas clases no están disponibles")
    
    for verificacion in verificaciones_clases:
        if "✓" in verificacion:
            print(f"  {Colors.GREEN}✓{Colors.RESET} {verificacion.replace(': ✓', '')}")
        else:
            print(f"  {Colors.RED}✗{Colors.RESET} {verificacion.replace(': ✗', '').split(' (')[0]}")
    
    # Verificar configuración
    print(f"\n{Colors.BOLD}4. Verificando configuración...{Colors.RESET}")
    config_ok, config_info = verificar_configuracion()
    print_status("Configuración", config_ok, config_info)
    
    # Ejecutar tests
    print(f"\n{Colors.BOLD}5. Ejecutando tests automatizados...{Colors.RESET}")
    tests_ok, tests_output = ejecutar_tests()
    print_status("Tests automatizados", tests_ok, "Tests pasaron correctamente" if tests_ok else "Algunos tests fallaron")
    
    if not tests_ok:
        print(f"  {Colors.YELLOW}Output de tests:{Colors.RESET}")
        for line in tests_output.split('\n')[:10]:  # Mostrar solo las primeras 10 líneas
            if line.strip():
                print(f"    {line}")
    
    # Resumen final
    print_header("RESUMEN DE VERIFICACIÓN")
    
    total_verificaciones = 5
    verificaciones_exitosas = sum([
        archivos_ok,
        importaciones_ok,
        clases_ok,
        config_ok,
        tests_ok
    ])
    
    porcentaje = (verificaciones_exitosas / total_verificaciones) * 100
    
    if porcentaje == 100:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ PROYECTO COMPLETAMENTE FUNCIONAL{Colors.RESET}")
        print(f"{Colors.GREEN}Todas las verificaciones pasaron exitosamente ({verificaciones_exitosas}/{total_verificaciones}){Colors.RESET}")
        print(f"{Colors.GREEN}El proyecto está listo para usar en modo v2.0{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}Comandos para ejecutar:{Colors.RESET}")
        print(f"{Colors.WHITE}  python main.py{Colors.RESET}          # Ejecutar aplicación v2.0")
        print(f"{Colors.WHITE}  python -m tests.test_refactor{Colors.RESET}  # Ejecutar tests")
        
    elif porcentaje >= 80:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  PROYECTO MAYORMENTE FUNCIONAL{Colors.RESET}")
        print(f"{Colors.YELLOW}La mayoría de verificaciones pasaron ({verificaciones_exitosas}/{total_verificaciones}){Colors.RESET}")
        print(f"{Colors.YELLOW}Hay algunos problemas menores que corregir{Colors.RESET}")
        
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ PROYECTO REQUIERE ATENCIÓN{Colors.RESET}")
        print(f"{Colors.RED}Solo {verificaciones_exitosas}/{total_verificaciones} verificaciones pasaron{Colors.RESET}")
        print(f"{Colors.RED}Se requieren correcciones antes de usar{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}Para más información, consulta:{Colors.RESET}")
    print(f"  - README.md (instrucciones de uso)")
    print(f"  - ARQUITECTURA_MODULAR.md (documentación técnica)")
    print(f"  - MIGRACION_V2.md (guía de migración)")

if __name__ == "__main__":
    main()
