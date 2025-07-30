"""
Aplicación principal de DotaTwin - Versión modular 3.0.

Este módulo contiene la clase principal de la aplicación que coordina
todos los componentes siguiendo principios de arquitectura limpia.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Optional
from pathlib import Path

# Imports locales
from .main_tab import AccountListWidget, StatusWidget, ActionButtonsWidget
from .ignored_tab import IgnoredTabController
from ..core.steam_service import SteamAccountService, AccountFilterService, ValidationService
from ..core.config_service import ConfigurationService, FileCopyService
from ..core.steam_config_service import SteamConfigurationService
from ..models.domain_models import SteamAccount, AppSelection, CopyOperation, AppConfig
from ..utils.ui_utils import MessageHelper, IconHelper, AboutDialog
from ..utils.logging_utils import LoggingMixin, OperationContext
from config.settings import (
    APP_NAME, APP_VERSION, APP_AUTHOR, APP_DESCRIPTION, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT, ICON_PATH, MESSAGES
)


class DotaTwinApp(LoggingMixin):
    """
    Aplicación principal de DotaTwin.
    
    Coordina todos los servicios y componentes de la interfaz,
    siguiendo el patrón MVC y principios de responsabilidad única.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Inicializa la aplicación principal.
        
        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        
        # Inicializar servicios
        self._init_services()
        
        # Estado de la aplicación
        self.all_accounts: List[SteamAccount] = []
        self.available_accounts: List[SteamAccount] = []
        self.ignored_accounts: List[SteamAccount] = []
        self.current_selection = AppSelection()
        
        # Componentes de interfaz
        self.main_tab_widget: Optional[AccountListWidget] = None
        self.ignored_tab_controller: Optional[IgnoredTabController] = None
        self.status_widget: Optional[StatusWidget] = None
        self.action_buttons: Optional[ActionButtonsWidget] = None
        
        # Configurar aplicación
        self._setup_application()
        self._create_interface()
        self._load_initial_data()
        
        # Establecer icono de barra de tareas después de la inicialización completa
        self.root.after(100, self._finalize_icon_setup)
    
    def _init_services(self) -> None:
        """Inicializa todos los servicios de la aplicación."""
        # Cargar configuración primero
        self.config_service = ConfigurationService()
        self.app_config = self.config_service.load_config()
        
        # Inicializar servicio de configuración de Steam
        self.steam_config_service = SteamConfigurationService(self.app_config)
        
        # Verificar instalación de Steam
        if not self.steam_config_service.detect_steam_installation():
            # Si no se detecta Steam, solicitar ubicación
            if not self.steam_config_service.prompt_steam_location(self.root):
                # Si el usuario cancela, mostrar advertencia pero continuar
                MessageHelper.show_warning(
                    "Steam no configurado",
                    "La aplicación funcionará con limitaciones.\\n"
                    "Puede configurar Steam más tarde desde el menú Configuración."
                )
        
        # Inicializar otros servicios
        self.steam_service = SteamAccountService(self.app_config.custom_steam_path)
        self.filter_service = AccountFilterService()
        self.validation_service = ValidationService()
        self.file_service = FileCopyService(enable_backup=True)
        
        self.logger.info("Servicios inicializados correctamente")
    
    def _setup_application(self) -> None:
        """Configura la ventana principal y propiedades de la aplicación."""
        # Configurar App ID para Windows (ayuda con el icono de barra de tareas)
        self._set_app_id()
        
        # Título de la ventana
        title = f"{APP_NAME} v{APP_VERSION} - {APP_AUTHOR}"
        self.root.title(title)
        
        # Tamaño y posición de ventana
        self.root.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # Icono de la aplicación
        icon_path = Path(ICON_PATH)
        if icon_path.exists():
            try:
                # Establecer icono para la ventana y barra de tareas de Windows
                self.root.iconbitmap(str(icon_path))
                
                # Para mejor compatibilidad con Windows, también configurar wm_iconbitmap
                self.root.wm_iconbitmap(str(icon_path))
                
                # Solución adicional para Windows: forzar icono en barra de tareas
                self._set_taskbar_icon(str(icon_path))
                
                self.logger.info(f"Icono cargado correctamente: {icon_path}")
                
            except tk.TclError as e:
                self.logger.warning(f"No se pudo cargar el icono: {icon_path} - {e}")
        else:
            self.logger.warning(f"Archivo de icono no encontrado: {icon_path}")
        
        # Configurar cierre de aplicación
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self.logger.info(f"Aplicación configurada: {title}")
    
    def _set_app_id(self) -> None:
        """
        Establece el App ID de Windows para mejorar la identificación de la aplicación.
        
        Esto ayuda a que Windows reconozca la aplicación como única y muestre
        el icono correcto en la barra de tareas.
        """
        try:
            import ctypes
            app_id = f"Sadohu.{APP_NAME}.{APP_VERSION}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            self.logger.info(f"App ID establecido: {app_id}")
        except Exception as e:
            self.logger.warning(f"No se pudo establecer App ID: {e}")
    
    def _set_taskbar_icon(self, icon_path: str) -> None:
        """
        Establece el icono en la barra de tareas de Windows usando la API de Windows.
        
        Args:
            icon_path: Ruta al archivo de icono
        """
        try:
            import ctypes
            from ctypes import wintypes
            
            # Obtener el handle de la ventana
            hwnd = self.root.winfo_id()
            
            # Cargar el icono desde el archivo
            hicon = ctypes.windll.user32.LoadImageW(
                None,  # hInst (None para cargar desde archivo)
                icon_path,  # name (ruta del archivo)
                1,  # type (IMAGE_ICON)
                0,  # cx (ancho, 0 = tamaño por defecto)
                0,  # cy (alto, 0 = tamaño por defecto) 
                0x00000010 | 0x00000020  # flags (LR_LOADFROMFILE | LR_DEFAULTSIZE)
            )
            
            if hicon:
                # WM_SETICON messages
                ICON_SMALL = 0
                ICON_BIG = 1
                WM_SETICON = 0x0080
                
                # Establecer icono pequeño y grande
                ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
                ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
                
                self.logger.info("Icono de barra de tareas establecido correctamente")
            else:
                self.logger.warning("No se pudo cargar el icono para la barra de tareas")
                
        except ImportError:
            self.logger.info("ctypes no disponible, usando método estándar de Tkinter")
        except Exception as e:
            self.logger.warning(f"Error al establecer icono de barra de tareas: {e}")
    
    def _finalize_icon_setup(self) -> None:
        """
        Finaliza la configuración del icono después de que la ventana esté completamente cargada.
        """
        icon_path = Path(ICON_PATH)
        if icon_path.exists():
            try:
                # Intentar establecer el icono nuevamente
                self._set_taskbar_icon(str(icon_path))
                
                # Forzar actualización de la ventana
                self.root.update_idletasks()
                
            except Exception as e:
                self.logger.warning(f"Error en finalización de icono: {e}")
    
    def _create_menu(self) -> None:
        """Crea la barra de menú de la aplicación."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Recargar cuentas", command=self._reload_accounts)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self._on_closing)
        
        # Menú Configuración
        config_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Configuración", menu=config_menu)
        config_menu.add_command(label="Configurar Steam...", command=self._configure_steam)
        config_menu.add_separator()
        config_menu.add_command(label="Detectar Steam automáticamente", command=self._auto_detect_steam)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de...", command=self._show_about)
    
    def _create_interface(self) -> None:
        """Crea la interfaz de usuario completa."""
        with OperationContext("create_interface", self.logger):
            # Crear menú
            self._create_menu()
            
            # Frame principal que contendrá todo
            main_container = ttk.Frame(self.root)
            main_container.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Configurar grid del container principal para reservar espacio
            main_container.grid_rowconfigure(0, weight=1)  # Notebook expansible
            main_container.grid_rowconfigure(1, weight=0)  # Status fijo
            main_container.grid_rowconfigure(2, weight=0)  # Botones fijo
            main_container.grid_columnconfigure(0, weight=1)
            
            # Crear notebook para pestañas (se expande pero respeta espacio reservado)
            self.notebook = ttk.Notebook(main_container)
            self.notebook.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
            
            # Crear pestañas
            self._create_main_tab()
            self._create_ignored_tab()
            
            # Crear widgets de estado y acciones en posiciones fijas
            self._create_status_widgets(main_container)
    
    def _create_main_tab(self) -> None:
        """Crea la pestaña principal de cuentas disponibles."""
        # Frame de la pestaña
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="Cuentas Disponibles")
        
        # Widget principal de lista de cuentas
        self.main_tab_widget = AccountListWidget(
            main_frame, 
            "Cuentas Steam con Dota 2 detectadas"
        )
        
        # Configurar callbacks
        self.main_tab_widget.on_selection_changed = self._on_selection_changed
        self.main_tab_widget.on_account_ignored = self._on_account_ignored
    
    def _create_ignored_tab(self) -> None:
        """Crea la pestaña de cuentas ignoradas."""
        # Frame de la pestaña
        ignored_frame = ttk.Frame(self.notebook)
        self.notebook.add(ignored_frame, text="Cuentas Ignoradas")
        
        # Controlador de la pestaña ignoradas
        self.ignored_tab_controller = IgnoredTabController(ignored_frame)
        self.ignored_tab_controller.on_account_restored = self._on_account_restored
    
    def _create_status_widgets(self, parent: tk.Widget) -> None:
        """Crea los widgets de estado y botones de acción en posiciones fijas."""
        # Widget de estado - posición fija en row=1
        self.status_widget = StatusWidget(parent)
        self.status_widget.position_fixed(row=1, column=0)
        
        # Botones de acción - posición fija en row=2
        self.action_buttons = ActionButtonsWidget(parent)
        self.action_buttons.position_fixed(row=2, column=0)
        self.action_buttons.on_copy_clicked = self._on_copy_configuration
        self.action_buttons.on_cancel_clicked = self._on_cancel_selection
    
    def _load_initial_data(self) -> None:
        """Carga los datos iniciales de la aplicación."""
        with OperationContext("load_initial_data", self.logger):
            # Validar instalación de Steam
            is_valid, error_msg = self.validation_service.validate_steam_paths()
            if not is_valid:
                MessageHelper.show_error("Error", error_msg)
                return
            
            # Detectar cuentas de Steam
            self.all_accounts = self.steam_service.find_accounts_with_dota2()
            
            if not self.all_accounts:
                MessageHelper.show_warning("Aviso", MESSAGES["no_accounts"])
                return
            
            # Cargar configuración guardada
            self._load_saved_configuration()
            
            # Actualizar interfaz
            self._refresh_account_lists()
            self._restore_previous_selection()
    
    def _load_saved_configuration(self) -> None:
        """Carga la configuración guardada previamente."""
        # Configurar paginación en widgets
        if self.main_tab_widget:
            self.main_tab_widget.pagination.items_per_page = self.app_config.items_por_pagina
        
        if self.ignored_tab_controller:
            self.ignored_tab_controller.set_items_per_page(self.app_config.items_por_pagina)
        
        self.logger.info("Configuración cargada correctamente")
    
    def _refresh_account_lists(self) -> None:
        """Actualiza las listas de cuentas disponibles e ignoradas."""
        ignored_ids = self.app_config.cuentas_ignoradas
        
        # Filtrar cuentas
        self.available_accounts = self.filter_service.filter_available_accounts(
            self.all_accounts, ignored_ids
        )
        self.ignored_accounts = self.filter_service.filter_ignored_accounts(
            self.all_accounts, ignored_ids
        )
        
        # Actualizar widgets y forzar redibujado
        if self.main_tab_widget:
            self.main_tab_widget.set_accounts(self.available_accounts)
            # Forzar actualización visual
            self.main_tab_widget.parent.update_idletasks()
        
        if self.ignored_tab_controller:
            self.ignored_tab_controller.set_ignored_accounts(self.ignored_accounts)
            # Forzar actualización visual
            self.ignored_tab_controller.accounts_list.parent.update_idletasks()
        
        # Actualizar la ventana completa
        self.root.update_idletasks()
        
        self.logger.info(f"Listas actualizadas: {len(self.available_accounts)} disponibles, "
                        f"{len(self.ignored_accounts)} ignoradas")
    
    def _restore_previous_selection(self) -> None:
        """Restaura la selección previa guardada."""
        config = self.config_service.config
        
        # Buscar cuentas de la selección previa
        if config.origen:
            origen_account = self.filter_service.find_account_by_id(
                self.available_accounts, config.origen
            )
            if origen_account:
                self.current_selection.set_origen(origen_account)
                # Navegar a la página de la cuenta origen
                if self.main_tab_widget:
                    self.main_tab_widget.navigate_to_account(origen_account)
        
        if config.destino:
            destino_account = self.filter_service.find_account_by_id(
                self.available_accounts, config.destino
            )
            if destino_account:
                self.current_selection.set_destino(destino_account)
                # Si no hay origen, navegar a destino
                if not self.current_selection.origen and self.main_tab_widget:
                    self.main_tab_widget.navigate_to_account(destino_account)
        
        # Actualizar interfaz con selección restaurada
        self._update_ui_selection()
        
        if self.current_selection.is_complete:
            self.logger.info("Selección previa restaurada correctamente")
    
    def _update_ui_selection(self) -> None:
        """Actualiza la interfaz con la selección actual."""
        # Actualizar widget principal
        if self.main_tab_widget:
            self.main_tab_widget.set_selection(self.current_selection)
        
        # Actualizar widget de estado
        if self.status_widget:
            self.status_widget.update_status(self.current_selection)
        
        # Actualizar botones de acción
        if self.action_buttons:
            self.action_buttons.update_selection(self.current_selection)
    
    # ═══════════════════════════════════════════════════════════════════════
    # Event Handlers
    # ═══════════════════════════════════════════════════════════════════════
    
    def _on_selection_changed(self, selection: AppSelection) -> None:
        """
        Maneja el cambio en la selección de cuentas.
        
        Args:
            selection: Nueva selección
        """
        self.current_selection = selection
        
        # Guardar selección
        origen_id = selection.origen.steamid if selection.origen else ""
        destino_id = selection.destino.steamid if selection.destino else ""
        self.config_service.update_selection(origen_id, destino_id)
        
        # Actualizar interfaz
        self._update_ui_selection()
        
        self.log_method_call("selection_changed", 
                            origen=origen_id, destino=destino_id)
    
    def _on_account_ignored(self, account: SteamAccount) -> None:
        """
        Maneja la solicitud de ignorar una cuenta.
        
        Args:
            account: Cuenta a ignorar
        """
        # Verificar si la cuenta ya está ignorada
        if self.app_config.is_ignored(account.steamid):
            MessageHelper.show_info(
                "Cuenta ya ignorada",
                f"La cuenta '{account.nombre}' ya está en la lista de ignoradas.\\n\\n"
                f"Puedes verla en la pestaña 'Cuentas Ignoradas'."
            )
            return
        
        # Confirmar con el usuario (asegurar que el diálogo aparezca al frente)
        self.root.lift()  # Traer ventana al frente
        self.root.attributes('-topmost', True)  # Temporal: al frente
        
        confirm = MessageHelper.ask_confirmation(
            "Confirmar",
            MESSAGES["confirm_ignore"].format(account.nombre)
        )
        
        self.root.attributes('-topmost', False)  # Quitar topmost
        
        if not confirm:
            return
        
        # Ignorar cuenta
        self.config_service.ignore_account(account.steamid)
        
        # Actualizar referencia de configuración para sincronizar cambios
        self.app_config = self.config_service.config
        
        # Limpiar selección si la cuenta ignorada estaba seleccionada
        if self.current_selection.has_account(account):
            self.current_selection.clear()
            self._on_selection_changed(self.current_selection)
        
        # Actualizar listas
        self._refresh_account_lists()
        
        # Mostrar confirmación de éxito
        MessageHelper.show_info(
            "Cuenta ignorada",
            f"La cuenta '{account.nombre}' ha sido ignorada exitosamente.\\n\\n"
            f"Puedes restaurarla desde la pestaña 'Cuentas Ignoradas'."
        )
        
        self.log_method_call("account_ignored", account=account.steamid)
    
    def _on_account_restored(self, account: SteamAccount) -> None:
        """
        Maneja la restauración de una cuenta ignorada.
        
        Args:
            account: Cuenta a restaurar
        """
        # Restaurar cuenta
        self.config_service.restore_account(account.steamid)
        
        # Actualizar referencia de configuración para sincronizar cambios
        self.app_config = self.config_service.config
        
        # Actualizar listas
        self._refresh_account_lists()
        
        # Mostrar confirmación de éxito
        MessageHelper.show_info(
            "Cuenta restaurada",
            f"La cuenta '{account.nombre}' ha sido restaurada exitosamente.\\n\\n"
            f"Ahora aparece en la pestaña 'Cuentas Disponibles'."
        )
        
        self.log_method_call("account_restored", account=account.steamid)
    
    def _on_copy_configuration(self) -> None:
        """Maneja la solicitud de copiar configuración."""
        if not self.current_selection.is_valid:
            MessageHelper.show_error("Error", "Selección inválida para copia")
            return
        
        # Confirmar operación
        confirm = MessageHelper.ask_confirmation(
            "Confirmar",
            MESSAGES["confirm_copy"].format(
                self.current_selection.origen.nombre,
                self.current_selection.destino.nombre
            )
        )
        
        if not confirm:
            return
        
        # Crear operación de copia
        copy_operation = CopyOperation(
            origen=self.current_selection.origen,
            destino=self.current_selection.destino,
            backup_enabled=self.config_service.config.auto_backup
        )
        
        # Validar operación
        is_valid, error_msg = self.validation_service.validate_copy_operation(
            copy_operation.origen, copy_operation.destino
        )
        
        if not is_valid:
            MessageHelper.show_error("Error de validación", error_msg)
            return
        
        # Ejecutar copia
        with OperationContext("copy_configuration", self.logger):
            success, message = self.file_service.copy_configuration(copy_operation)
            
            if success:
                MessageHelper.show_info("Éxito", MESSAGES["success_copy"], "success")
                # Guardar selección exitosa
                self.config_service.update_selection(
                    self.current_selection.origen.steamid,
                    self.current_selection.destino.steamid
                )
            else:
                MessageHelper.show_error("Error", message)
        
        self.log_method_call("copy_configuration", 
                            success=success, message=message)
    
    def _on_cancel_selection(self) -> None:
        """Maneja la cancelación de la selección actual."""
        self.current_selection.clear()
        self._on_selection_changed(self.current_selection)
        
        self.log_method_call("cancel_selection")
    
    def _reload_accounts(self) -> None:
        """Recarga las cuentas de Steam."""
        with OperationContext("reload_accounts", self.logger):
            # Reinicializar servicio de Steam
            self.steam_service = SteamAccountService(self.app_config.custom_steam_path)
            
            # Recargar datos
            self._load_initial_data()
            
            MessageHelper.show_info("Cuentas recargadas", "Las cuentas de Steam han sido recargadas correctamente.")
    
    def _configure_steam(self) -> None:
        """Abre el diálogo de configuración de Steam."""
        result = self.steam_config_service.show_steam_configuration_dialog(self.root)
        if result:
            # Guardar configuración
            self.config_service.save_config(self.app_config)
            
            # Recargar cuentas con nueva configuración
            self._reload_accounts()
    
    def _auto_detect_steam(self) -> None:
        """Intenta detectar Steam automáticamente."""
        # Limpiar ruta personalizada para forzar detección automática
        old_path = self.app_config.custom_steam_path
        self.app_config.custom_steam_path = ""
        
        if self.steam_config_service.detect_steam_installation():
            # Guardar configuración actualizada
            self.config_service.save_config(self.app_config)
            
            # Recargar cuentas
            self._reload_accounts()
            
            MessageHelper.show_info(
                "Steam detectado",
                "Steam ha sido detectado automáticamente y las cuentas han sido recargadas."
            )
        else:
            # Restaurar ruta anterior si falla
            self.app_config.custom_steam_path = old_path
            
            MessageHelper.show_warning(
                "Steam no detectado",
                "No se pudo detectar Steam automáticamente.\\n"
                "Use 'Configurar Steam...' para seleccionar la ubicación manualmente."
            )
    
    def _show_about(self) -> None:
        """Muestra información sobre la aplicación."""
        about_text = f"""{APP_NAME} v{APP_VERSION}
Desarrollado por {APP_AUTHOR}

{APP_DESCRIPTION}

🎯 Twin your Dota experience - Crea gemelos perfectos de tus configuraciones

Arquitectura Modular v3.0
- Separación de responsabilidades
- Principios SOLID aplicados
- Testing automatizado
- Logging avanzado
- Layout responsivo con Grid
- Sistema de ignorar cuentas
- Copia completa de configuraciones

📞 Contacto y Soporte:
Discord: Sadohu
🔗 Unirse al Discord: https://discord.gg/MYNyKQvk
GitHub: Sadohu

🔗 Repositorio del Proyecto:
https://github.com/sadohu/DotaTwin

Steam configurado en: {self.app_config.custom_steam_path or 'Detección automática'}"""
        
        # Usar el nuevo diálogo personalizado
        dialog = AboutDialog(self.root, "Acerca de", about_text)
        dialog.show()
    
    def _on_closing(self) -> None:
        """Maneja el cierre de la aplicación."""
        with OperationContext("application_closing", self.logger):
            # Guardar configuración final
            geometry = self.root.geometry()
            self.config_service.update_window_geometry(geometry)
            
            # Limpiar recursos
            self._cleanup_resources()
            
            # Cerrar aplicación
            self.root.destroy()
    
    def _cleanup_resources(self) -> None:
        """Limpia recursos antes del cierre."""
        # Limpiar caché de avatares
        if self.main_tab_widget:
            self.main_tab_widget.avatar_manager.clear_cache()
        
        if self.ignored_tab_controller:
            self.ignored_tab_controller.accounts_list.avatar_manager.clear_cache()
        
        # Limpiar backups antiguos
        self.file_service.cleanup_old_backups()
        
        self.logger.info("Recursos limpiados correctamente")
    
    # ═══════════════════════════════════════════════════════════════════════
    # Public API
    # ═══════════════════════════════════════════════════════════════════════
    
    def refresh_accounts(self) -> None:
        """
        Actualiza la lista de cuentas detectadas.
        
        Método público para refrescar la detección de cuentas.
        """
        with OperationContext("refresh_accounts", self.logger):
            self.all_accounts = self.steam_service.find_accounts_with_dota2()
            self._refresh_account_lists()
    
    def get_application_info(self) -> dict:
        """
        Obtiene información de la aplicación.
        
        Returns:
            Diccionario con información de la aplicación
        """
        return {
            "name": APP_NAME,
            "version": APP_VERSION,
            "author": APP_AUTHOR,
            "accounts_detected": len(self.all_accounts),
            "accounts_available": len(self.available_accounts),
            "accounts_ignored": len(self.ignored_accounts),
            "current_selection": {
                "origen": self.current_selection.origen.steamid if self.current_selection.origen else None,
                "destino": self.current_selection.destino.steamid if self.current_selection.destino else None,
                "is_valid": self.current_selection.is_valid
            }
        }


def main():
    """
    Función principal para ejecutar la aplicación.
    
    Punto de entrada principal del programa.
    """
    from ..utils.logging_utils import setup_logging
    
    # Configurar logging
    setup_logging("INFO")
    
    # Crear ventana principal
    root = tk.Tk()
    
    try:
        # Crear y ejecutar aplicación
        app = DotaTwinApp(root)
        
        # Mostrar información inicial
        app_info = app.get_application_info()
        app.logger.info(f"Aplicación iniciada: {app_info}")
        
        # Ejecutar loop principal
        root.mainloop()
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fatal en la aplicación: {e}", exc_info=True)
        
        # Mostrar error al usuario
        MessageHelper.show_error(
            "Error Fatal",
            f"La aplicación encontró un error fatal:\n{e}\n\n"
            f"Consulta el archivo de log para más detalles."
        )
    
    finally:
        # Asegurar que la ventana se cierre
        try:
            root.destroy()
        except:
            pass


if __name__ == "__main__":
    main()
