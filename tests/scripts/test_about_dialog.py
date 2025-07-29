#!/usr/bin/env python3
"""
Script de prueba para el nuevo diálogo 'Acerca de...' personalizado.
"""

import tkinter as tk
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.ui_utils import AboutDialog

def test_about_dialog():
    """Prueba el nuevo diálogo 'Acerca de...' personalizado."""
    print("🧪 PROBANDO DIÁLOGO 'ACERCA DE...' PERSONALIZADO")
    print("=" * 50)
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("Test - Diálogo Acerca de")
    root.geometry("400x300")
    
    # Contenido de prueba
    about_text = """Dota 2 Config Copier v2.1.1
Desarrollado por Sadohu

Aplicación para copiar configuraciones de Dota 2 entre cuentas de Steam

Arquitectura Modular v2.1
- Separación de responsabilidades
- Principios SOLID aplicados
- Testing automatizado
- Logging avanzado
- Layout responsivo con Grid
- Sistema de ignorar cuentas

📞 Contacto y Soporte:
Discord: Sadohu
GitHub: Sadohu

🔗 Repositorio del Proyecto:
https://github.com/sadohu/Dota2CopyMainConfig

Steam configurado en: Detección automática"""
    
    def show_dialog():
        """Muestra el diálogo de prueba."""
        dialog = AboutDialog(root, "Acerca de - Dota 2 Config Copier", about_text)
        dialog.show()
    
    # Botón para mostrar diálogo
    btn_frame = tk.Frame(root)
    btn_frame.pack(expand=True)
    
    test_btn = tk.Button(
        btn_frame,
        text="🔍 Mostrar Diálogo 'Acerca de...'",
        command=show_dialog,
        font=("Arial", 12),
        bg="lightblue",
        pady=10,
        padx=20
    )
    test_btn.pack(pady=20)
    
    info_label = tk.Label(
        btn_frame,
        text="Pruebas a realizar:\n\n"
             "✅ Texto seleccionable\n"
             "✅ Enlace clicable (GitHub)\n"
             "✅ Botón 'Copiar Info'\n"
             "✅ Nombres de contacto resaltados\n"
             "✅ Scroll si es necesario",
        font=("Arial", 10),
        justify="left",
        bg="lightyellow",
        pady=10,
        padx=10
    )
    info_label.pack(pady=10)
    
    print("📋 Instrucciones de prueba:")
    print("1. Haz clic en 'Mostrar Diálogo Acerca de...'")
    print("2. Verifica que puedes seleccionar texto")
    print("3. Haz clic en el enlace de GitHub")
    print("4. Prueba el botón 'Copiar Info'")
    print("5. Verifica que los nombres están resaltados")
    print("\n▶️ Iniciando prueba...")
    
    try:
        root.mainloop()
        print("✅ Prueba completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_about_dialog()
