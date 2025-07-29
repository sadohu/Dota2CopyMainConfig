#!/usr/bin/env python3
"""
Test script para verificar la funcionalidad del AboutDialog mejorado.
"""

import tkinter as tk
from src.utils.ui_utils import AboutDialog

def test_about_dialog():
    """Prueba el AboutDialog con todas sus funcionalidades."""
    # Crear ventana principal de prueba
    root = tk.Tk()
    root.title("Test AboutDialog")
    root.geometry("400x300")
    
    def show_about():
        """Muestra el diálogo About."""
        content = """Dota 2 Config Copier v2.1.1

Este programa permite copiar configuraciones entre cuentas de Dota 2 de forma rápida y segura.

📧 Contacto:
• Discord: Sadohu
• GitHub: Sadohu
• Repositorio: https://github.com/sadohu/Dota2CopyMainConfig
• 🔗 Unirse al Discord: https://discord.gg/MYNyKQvk

✨ Características principales:
• Copia automática de configuraciones
• Interfaz intuitiva y fácil de usar
• Respaldo de seguridad automático
• Soporte para múltiples cuentas

Desarrollado con ❤️ para la comunidad de Dota 2"""
        
        about_dialog = AboutDialog(root, title="Acerca de Dota 2 Config Copier", content=content)
        about_dialog.show()
    
    # Botón para mostrar el diálogo
    btn_about = tk.Button(
        root,
        text="Mostrar Diálogo About",
        command=show_about,
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=10
    )
    btn_about.pack(expand=True)
    
    # Instrucciones
    instructions = tk.Label(
        root,
        text="Haz clic en el botón para probar el AboutDialog mejorado.\n\n"
             "Funcionalidades a probar:\n"
             "• Texto seleccionable\n"
             "• Enlaces clickeables (GitHub y Discord)\n"
             "• Botón de copiar información de contacto\n"
             "• Botón de cerrar",
        justify=tk.LEFT,
        font=("Arial", 10),
        wraplength=350
    )
    instructions.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    test_about_dialog()
