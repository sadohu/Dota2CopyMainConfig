#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de ignorar cuentas.
"""

import tkinter as tk
import logging
from src.gui.main_app import Dota2ConfigCopierApp
from src.utils.logging_utils import setup_logging

def test_ignore_functionality():
    """Prueba la funcionalidad de ignorar cuentas."""
    print("🧪 PROBANDO FUNCIONALIDAD DE IGNORAR CUENTAS")
    print("=" * 50)
    
    # Configurar logging para ver detalles
    setup_logging("DEBUG")
    
    # Crear ventana principal
    root = tk.Tk()
    
    try:
        # Crear aplicación
        app = Dota2ConfigCopierApp(root)
        
        # Información inicial
        app_info = app.get_application_info()
        print(f"\n📊 ESTADO INICIAL:")
        print(f"   • Total de cuentas: {app_info['accounts_detected']}")
        print(f"   • Cuentas disponibles: {app_info['accounts_available']}")
        print(f"   • Cuentas ignoradas: {app_info['accounts_ignored']}")
        
        # Verificar archivo de configuración
        config = app.config_service.config
        print(f"\n📁 CONFIGURACIÓN ACTUAL:")
        print(f"   • Cuentas ignoradas en config: {config.cuentas_ignoradas}")
        print(f"   • Items por página: {config.items_por_pagina}")
        
        # Verificar si hay cuentas disponibles para ignorar
        if app.available_accounts:
            first_account = app.available_accounts[0]
            print(f"\n🎯 CUENTA DE PRUEBA:")
            print(f"   • SteamID: {first_account.steamid}")
            print(f"   • Nombre: {first_account.nombre}")
            
            # Verificar callback de ignorar
            main_tab = app.main_tab_widget
            if main_tab and hasattr(main_tab, 'on_account_ignored'):
                print(f"   • Callback configurado: ✅")
                
                # Intentar simular ignorar
                print(f"\n⚡ SIMULANDO IGNORAR CUENTA...")
                try:
                    app._on_account_ignored(first_account)
                    print(f"   • Función ejecutada correctamente")
                    
                    # Verificar estado después
                    new_info = app.get_application_info()
                    print(f"   • Cuentas disponibles después: {new_info['accounts_available']}")
                    print(f"   • Cuentas ignoradas después: {new_info['accounts_ignored']}")
                    
                except Exception as e:
                    print(f"   • ❌ Error al ignorar: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"   • ❌ Callback NO configurado")
        else:
            print(f"\n⚠️  No hay cuentas disponibles para probar")
        
        # Verificar widgets de la interfaz
        print(f"\n🖥️  VERIFICACIÓN DE WIDGETS:")
        if hasattr(app, 'main_tab_widget') and app.main_tab_widget:
            print(f"   • main_tab_widget: ✅")
            if hasattr(app.main_tab_widget, 'account_widgets'):
                print(f"   • account_widgets: {len(app.main_tab_widget.account_widgets)} widgets")
                
                # Verificar primer widget si existe
                if app.main_tab_widget.account_widgets:
                    first_widget = app.main_tab_widget.account_widgets[0]
                    if hasattr(first_widget, 'btn_ignorar'):
                        print(f"   • btn_ignorar en primer widget: ✅")
                        if hasattr(first_widget, 'on_ignore_account'):
                            print(f"   • callback on_ignore_account: ✅")
                        else:
                            print(f"   • callback on_ignore_account: ❌")
                    else:
                        print(f"   • btn_ignorar en primer widget: ❌")
            else:
                print(f"   • account_widgets: ❌")
        else:
            print(f"   • main_tab_widget: ❌")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            root.destroy()
        except:
            pass
    
    print(f"\n🏁 PRUEBA COMPLETADA")

if __name__ == "__main__":
    test_ignore_functionality()
