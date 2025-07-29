#!/usr/bin/env python3
"""
Script de prueba específico para el diálogo de confirmación.
"""

import tkinter as tk
from src.utils.ui_utils import MessageHelper

def test_confirmation_dialog():
    """Prueba el diálogo de confirmación."""
    print("🧪 PROBANDO DIÁLOGO DE CONFIRMACIÓN")
    print("=" * 40)
    
    # Crear ventana principal
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    try:
        print("📋 Mostrando diálogo de confirmación...")
        
        # Probar diálogo de confirmación
        result = MessageHelper.ask_confirmation(
            "Confirmar",
            "¿Deseas ignorar la cuenta 'TestAccount'?\\n\\nPodrás restaurarla desde la pestaña 'Cuentas Ignoradas'."
        )
        
        print(f"✅ Resultado del diálogo: {result}")
        
        if result:
            print("🎯 Usuario confirmó la acción")
        else:
            print("❌ Usuario canceló la acción")
            
    except Exception as e:
        print(f"❌ Error en diálogo: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    test_confirmation_dialog()
