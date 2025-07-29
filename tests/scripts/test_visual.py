#!/usr/bin/env python3
"""
Script de prueba visual para verificar el layout de la interfaz.
Ejecuta el programa y muestra información sobre la disposición de elementos.
"""

import tkinter as tk
from tkinter import ttk
import time
import threading
from src.gui.main_app import Dota2ConfigCopierApp
from src.utils.logging_utils import setup_logging

def test_layout():
    """Prueba visual del layout de la aplicación."""
    print("🧪 INICIANDO PRUEBA VISUAL DEL LAYOUT")
    print("=" * 50)
    
    # Configurar logging
    setup_logging()
    
    # Crear ventana principal
    root = tk.Tk()
    
    # Crear aplicación
    app = Dota2ConfigCopierApp(root)
    
    def check_widgets():
        """Verifica que todos los widgets estén visibles."""
        time.sleep(2)  # Esperar a que la interfaz se cargue completamente
        
        try:
            # Verificar que los widgets principales existen
            widgets_status = {
                "Ventana principal": root.winfo_exists(),
                "Notebook (pestañas)": hasattr(app, 'notebook') and app.notebook.winfo_exists(),
                "Widget de estado": hasattr(app, 'status_widget') and app.status_widget.status_label.winfo_exists(),
                "Botones de acción": hasattr(app, 'action_buttons') and app.action_buttons.btn_copiar.winfo_exists(),
                "Lista de cuentas": hasattr(app, 'main_tab_widget') and app.main_tab_widget.title_label.winfo_exists()
            }
            
            print("\n📊 ESTADO DE LOS WIDGETS:")
            for widget_name, exists in widgets_status.items():
                status = "✅ VISIBLE" if exists else "❌ NO VISIBLE"
                print(f"  {widget_name}: {status}")
            
            # Verificar geometría de la ventana
            geometry = root.geometry()
            print(f"\n📐 GEOMETRÍA DE LA VENTANA: {geometry}")
            
            # Verificar posición de widgets críticos
            if hasattr(app, 'status_widget') and app.status_widget.status_label.winfo_exists():
                status_y = app.status_widget.status_label.winfo_y()
                print(f"📍 Posición Y del widget de estado: {status_y}")
            
            if hasattr(app, 'action_buttons') and app.action_buttons.btn_copiar.winfo_exists():
                button_y = app.action_buttons.btn_copiar.winfo_y()
                print(f"📍 Posición Y de los botones: {button_y}")
            
            # Verificar si todos los widgets están dentro del área visible
            window_height = root.winfo_height()
            print(f"📏 Altura de la ventana: {window_height}px")
            
            all_visible = all(widgets_status.values())
            if all_visible:
                print("\n🎉 RESULTADO: TODOS LOS WIDGETS SON VISIBLES")
                print("✅ El problema del layout ha sido CORREGIDO")
            else:
                print("\n⚠️  RESULTADO: ALGUNOS WIDGETS NO SON VISIBLES")
                print("❌ El problema del layout AÚN PERSISTE")
                
        except Exception as e:
            print(f"\n❌ ERROR durante la verificación: {e}")
        
        # Cerrar la aplicación después de la prueba
        root.after(1000, root.quit)  # Cerrar después de 1 segundo
    
    # Ejecutar verificación en hilo separado
    thread = threading.Thread(target=check_widgets)
    thread.daemon = True
    thread.start()
    
    # Ejecutar el mainloop de la aplicación
    try:
        app.run()
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")
    
    print("\n🏁 PRUEBA VISUAL COMPLETADA")

if __name__ == "__main__":
    test_layout()
