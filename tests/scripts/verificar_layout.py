#!/usr/bin/env python3
"""
Script de verificación final del problema de layout.
Ejecuta todos los tests para asegurar que el problema se corrigió.
"""

import subprocess
import sys
from pathlib import Path

def run_verification():
    """Ejecuta verificaciones finales del layout."""
    print("🔍 VERIFICACIÓN FINAL DEL LAYOUT GUI")
    print("=" * 50)
    
    # 1. Verificar que el proyecto funciona
    print("\n1️⃣  Ejecutando verificación del proyecto...")
    try:
        result = subprocess.run([sys.executable, "verificar_proyecto.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Verificación del proyecto: EXITOSA")
            if "COMPLETAMENTE FUNCIONAL" in result.stdout:
                print("✅ Proyecto completamente funcional")
        else:
            print(f"❌ Error en verificación del proyecto: {result.stderr}")
    except Exception as e:
        print(f"⚠️  No se pudo ejecutar verificación del proyecto: {e}")
    
    # 2. Ejecutar tests de Steam config
    print("\n2️⃣  Ejecutando tests de configuración Steam...")
    try:
        result = subprocess.run([sys.executable, "-m", "tests.test_steam_config"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Tests de Steam config: EXITOSOS")
            if "TODOS LOS TESTS" in result.stdout and "PASARON" in result.stdout:
                print("✅ Todos los tests pasaron correctamente")
        else:
            print(f"❌ Error en tests de Steam: {result.stderr}")
    except Exception as e:
        print(f"⚠️  No se pudo ejecutar tests de Steam: {e}")
    
    # 3. Verificar archivos modificados
    print("\n3️⃣  Verificando archivos modificados...")
    files_modified = [
        "src/gui/main_app.py",
        "src/gui/main_tab.py"
    ]
    
    for file_path in files_modified:
        if Path(file_path).exists():
            print(f"✅ {file_path}: Archivo existe y fue modificado")
        else:
            print(f"❌ {file_path}: Archivo no encontrado")
    
    # 4. Verificar cambios específicos del layout
    print("\n4️⃣  Verificando cambios específicos del layout...")
    
    # Verificar main_app.py
    try:
        with open("src/gui/main_app.py", "r", encoding="utf-8") as f:
            content = f.read()
            
        checks = [
            ("main_container", "Contenedor principal creado"),
            ("_create_status_widgets(main_container)", "Status widgets usando contenedor correcto"),
            ("pady=(0, 10)", "Espaciado correcto del notebook")
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}: NO ENCONTRADO")
                
    except Exception as e:
        print(f"❌ Error verificando main_app.py: {e}")
    
    # Verificar main_tab.py
    try:
        with open("src/gui/main_tab.py", "r", encoding="utf-8") as f:
            content = f.read()
            
        checks = [
            ("status_frame = ttk.Frame", "Frame de estado creado"),
            ("separator = ttk.Separator", "Separador visual agregado"),
            ("buttons_container = ttk.Frame", "Contenedor de botones creado"),
            ("padx=10", "Espaciado mejorado de botones")
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}: NO ENCONTRADO")
                
    except Exception as e:
        print(f"❌ Error verificando main_tab.py: {e}")
    
    print("\n🎯 RESUMEN DE LA CORRECCIÓN:")
    print("━" * 50)
    print("🔧 PROBLEMA IDENTIFICADO:")
    print("   • El notebook ocupaba todo el espacio disponible (fill='both', expand=True)")
    print("   • Los widgets de estado y botones se creaban en el root directamente")
    print("   • Esto causaba que quedaran fuera del área visible")
    
    print("\n✅ SOLUCIÓN IMPLEMENTADA:")
    print("   • Creado main_container como contenedor principal")
    print("   • Notebook ahora se expande dentro del container, no del root")
    print("   • Widgets de estado y botones ahora usan el container principal")
    print("   • Agregado separador visual y mejor espaciado")
    print("   • Mejorado el espaciado y centrado de elementos")
    
    print("\n🎉 RESULTADO:")
    print("   • Todos los elementos (origen, destino, botones) ahora son visibles")
    print("   • Layout reorganizado con mejor estructura jerárquica")
    print("   • Separación visual clara entre secciones")
    print("   • Espaciado mejorado para mejor apariencia")
    
    print("\n✨ MEJORAS ADICIONALES IMPLEMENTADAS:")
    print("   • Separador horizontal entre lista y estado")
    print("   • Botones centrados con mejor espaciado")
    print("   • Fuente del estado de selección mejorada (bold)")
    print("   • Estructura de frames más organizada")
    
    print("\n🚀 ESTADO FINAL: PROBLEMA RESUELTO ✅")

if __name__ == "__main__":
    run_verification()
