"""
Utilidades de interfaz de usuario para la aplicación Dota 2 Config Copier.

Este módulo contiene helpers y utilidades para la construcción
de la interfaz gráfica, siguiendo principios DRY y reutilización.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, Callable, List, Tuple
from PIL import Image, ImageTk
from pathlib import Path
from ..models.domain_models import SteamAccount, PaginationInfo
from config.settings import ICONS, COLORS, AVATAR_SIZE, DEFAULT_AVATAR_COLOR


class StyleManager:
    """
    Gestor centralizado de estilos para la interfaz.
    
    Proporciona configuración consistente de estilos TTK.
    """
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.style = ttk.Style(root)
        self._setup_styles()
    
    def _setup_styles(self) -> None:
        """Configura todos los estilos de la aplicación."""
        # Estilos para frames de cuenta
        self.style.configure("Origen.TFrame", background=COLORS["origen"])
        self.style.configure("Destino.TFrame", background=COLORS["destino"])
        self.style.configure("Normal.TFrame", background=COLORS["normal"])
        self.style.configure("Ignorada.TFrame", background=COLORS["ignorada"])
        
        # Estilo para página seleccionada
        self.style.configure("Selected.TLabel", 
                           background=COLORS["selected_page"],
                           relief="raised")
    
    def apply_account_style(self, frame: ttk.Frame, style_type: str) -> None:
        """
        Aplica un estilo específico a un frame de cuenta.
        
        Args:
            frame: Frame a estilizar
            style_type: Tipo de estilo ("origen", "destino", "normal", "ignorada")
        """
        style_map = {
            "origen": "Origen.TFrame",
            "destino": "Destino.TFrame", 
            "normal": "Normal.TFrame",
            "ignorada": "Ignorada.TFrame"
        }
        
        style_name = style_map.get(style_type, "Normal.TFrame")
        frame.configure(style=style_name)


class AvatarManager:
    """
    Gestor de avatares para cuentas de Steam.
    
    Maneja la carga, redimensionado y caché de avatares.
    """
    
    def __init__(self):
        self._avatar_cache: Dict[str, ImageTk.PhotoImage] = {}
        self._default_avatar: Optional[ImageTk.PhotoImage] = None
    
    def get_avatar(self, account: SteamAccount) -> ImageTk.PhotoImage:
        """
        Obtiene el avatar de una cuenta, usando caché cuando sea posible.
        
        Args:
            account: Cuenta de Steam
            
        Returns:
            Avatar como PhotoImage
        """
        # Usar caché si existe
        if account.steamid in self._avatar_cache:
            return self._avatar_cache[account.steamid]
        
        # Cargar avatar
        if account.has_avatar:
            avatar = self._load_avatar_from_file(account.avatar)
        else:
            avatar = self._get_default_avatar()
        
        # Guardar en caché
        self._avatar_cache[account.steamid] = avatar
        return avatar
    
    def _load_avatar_from_file(self, avatar_path: Path) -> ImageTk.PhotoImage:
        """Carga un avatar desde archivo."""
        try:
            img = Image.open(avatar_path).resize(AVATAR_SIZE, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return self._get_default_avatar()
    
    def _get_default_avatar(self) -> ImageTk.PhotoImage:
        """Obtiene o crea el avatar por defecto."""
        if self._default_avatar is None:
            img = Image.new("RGB", AVATAR_SIZE, DEFAULT_AVATAR_COLOR)
            self._default_avatar = ImageTk.PhotoImage(img)
        
        return self._default_avatar
    
    def clear_cache(self) -> None:
        """Limpia el caché de avatares."""
        self._avatar_cache.clear()
    
    def preload_avatars(self, accounts: List[SteamAccount]) -> None:
        """
        Precarga avatares para una lista de cuentas.
        
        Args:
            accounts: Lista de cuentas
        """
        for account in accounts:
            self.get_avatar(account)


class IconHelper:
    """
    Helper para iconos Unicode de la interfaz.
    
    Proporciona acceso centralizado a iconos y texto con iconos.
    """
    
    @staticmethod
    def get_icon(icon_name: str) -> str:
        """
        Obtiene un icono por nombre.
        
        Args:
            icon_name: Nombre del icono
            
        Returns:
            Icono Unicode
        """
        return ICONS.get(icon_name, "")
    
    @staticmethod
    def text_with_icon(icon_name: str, text: str) -> str:
        """
        Combina un icono con texto.
        
        Args:
            icon_name: Nombre del icono
            text: Texto a combinar
            
        Returns:
            Texto con icono
        """
        icon = IconHelper.get_icon(icon_name)
        return f"{icon} {text}" if icon else text
    
    @staticmethod
    def create_icon_button(parent: tk.Widget, icon_name: str, text: str, 
                          command: Callable, **kwargs) -> ttk.Button:
        """
        Crea un botón con icono.
        
        Args:
            parent: Widget padre
            icon_name: Nombre del icono
            text: Texto del botón
            command: Función a ejecutar
            **kwargs: Argumentos adicionales para el botón
            
        Returns:
            Botón configurado
        """
        button_text = IconHelper.text_with_icon(icon_name, text)
        return ttk.Button(parent, text=button_text, command=command, **kwargs)


class PaginationWidget:
    """
    Widget reutilizable para paginación.
    
    Encapsula la lógica de navegación de páginas en un componente reutilizable.
    """
    
    def __init__(self, parent: tk.Widget, pagination: PaginationInfo, 
                 on_page_change: Callable[[int], None]):
        """
        Inicializa el widget de paginación.
        
        Args:
            parent: Widget padre
            pagination: Información de paginación
            on_page_change: Callback para cambio de página
        """
        self.parent = parent
        self.pagination = pagination
        self.on_page_change = on_page_change
        self.frame = ttk.Frame(parent)
        self._widgets: List[tk.Widget] = []
    
    def render(self) -> ttk.Frame:
        """
        Renderiza el widget de paginación.
        
        Returns:
            Frame contenedor
        """
        self._clear_widgets()
        
        if self.pagination.total_pages <= 1:
            return self.frame
        
        # Botón anterior
        if self.pagination.has_previous:
            btn_prev = IconHelper.create_icon_button(
                self.frame, "anterior", "Anterior",
                lambda: self._change_page(self.pagination.current_page - 1)
            )
            btn_prev.pack(side='left', padx=2)
            self._widgets.append(btn_prev)
        
        # Botones de páginas
        page_range = self.pagination.get_page_range()
        for page in page_range:
            if page == self.pagination.current_page:
                # Página actual como label
                lbl = tk.Label(self.frame, text=str(page), 
                             bg=COLORS["selected_page"], width=3, relief='raised')
                lbl.pack(side='left', padx=1)
                self._widgets.append(lbl)
            else:
                # Otras páginas como botones
                btn = ttk.Button(self.frame, text=str(page), width=3,
                               command=lambda p=page: self._change_page(p))
                btn.pack(side='left', padx=1)
                self._widgets.append(btn)
        
        # Botón siguiente
        if self.pagination.has_next:
            btn_next = IconHelper.create_icon_button(
                self.frame, "siguiente", "Siguiente",
                lambda: self._change_page(self.pagination.current_page + 1)
            )
            btn_next.pack(side='left', padx=2)
            self._widgets.append(btn_next)
        
        # Información de página
        info_label = tk.Label(self.frame, text=self.pagination.page_info_text)
        info_label.pack(side='right', padx=10)
        self._widgets.append(info_label)
        
        return self.frame
    
    def _change_page(self, new_page: int) -> None:
        """Cambia a una nueva página."""
        self.pagination.set_page(new_page)
        self.on_page_change(new_page)
        self.render()  # Re-renderizar para actualizar estado
    
    def _clear_widgets(self) -> None:
        """Limpia todos los widgets del frame."""
        for widget in self._widgets:
            widget.destroy()
        self._widgets.clear()


class MessageHelper:
    """
    Helper para mostrar mensajes de manera consistente.
    
    Centraliza la lógica de diálogos y notificaciones.
    """
    
    @staticmethod
    def show_info(title: str, message: str, icon_name: str = "info") -> None:
        """Muestra un mensaje informativo."""
        icon = IconHelper.get_icon(icon_name)
        full_message = f"{icon} {message}" if icon else message
        messagebox.showinfo(title, full_message)
    
    @staticmethod
    def show_warning(title: str, message: str, icon_name: str = "warning") -> None:
        """Muestra un mensaje de advertencia."""
        icon = IconHelper.get_icon(icon_name)
        full_message = f"{icon} {message}" if icon else message
        messagebox.showwarning(title, full_message)
    
    @staticmethod
    def show_error(title: str, message: str, icon_name: str = "error") -> None:
        """Muestra un mensaje de error."""
        icon = IconHelper.get_icon(icon_name)
        full_message = f"{icon} {message}" if icon else message
        messagebox.showerror(title, full_message)
    
    @staticmethod
    def ask_confirmation(title: str, message: str, 
                        icon_name: str = "info") -> bool:
        """
        Solicita confirmación del usuario.
        
        Returns:
            True si el usuario confirma
        """
        icon = IconHelper.get_icon(icon_name)
        full_message = f"{icon} {message}" if icon else message
        return messagebox.askyesno(title, full_message)


class ValidationHelper:
    """
    Helper para validaciones de interfaz de usuario.
    
    Proporciona validadores comunes para campos de entrada.
    """
    
    @staticmethod
    def validate_number(value: str, min_value: int = None, 
                       max_value: int = None) -> Tuple[bool, str]:
        """
        Valida que un valor sea un número en un rango específico.
        
        Args:
            value: Valor a validar
            min_value: Valor mínimo (opcional)
            max_value: Valor máximo (opcional)
            
        Returns:
            Tupla (es_válido, mensaje_error)
        """
        try:
            num = int(value)
            
            if min_value is not None and num < min_value:
                return False, f"El valor debe ser mayor o igual a {min_value}"
            
            if max_value is not None and num > max_value:
                return False, f"El valor debe ser menor o igual a {max_value}"
            
            return True, ""
            
        except ValueError:
            return False, "El valor debe ser un número entero"
    
    @staticmethod
    def validate_geometry(geometry: str) -> Tuple[bool, str]:
        """
        Valida una string de geometría de ventana.
        
        Args:
            geometry: String de geometría (ej: "800x600")
            
        Returns:
            Tupla (es_válido, mensaje_error)
        """
        try:
            if 'x' not in geometry:
                return False, "Formato inválido. Debe ser 'ANCHOxALTO'"
            
            width, height = geometry.split('x')
            width, height = int(width), int(height)
            
            if width < 400 or height < 300:
                return False, "Dimensiones mínimas: 400x300"
            
            if width > 3840 or height > 2160:
                return False, "Dimensiones máximas: 3840x2160"
            
            return True, ""
            
        except ValueError:
            return False, "Formato inválido. Debe ser 'ANCHOxALTO'"


class WidgetFactory:
    """
    Factory para crear widgets comunes de manera consistente.
    
    Centraliza la creación de widgets con configuraciones estándar.
    """
    
    @staticmethod
    def create_labeled_entry(parent: tk.Widget, label_text: str, 
                           icon_name: str = None, **entry_kwargs) -> Tuple[tk.Label, tk.Entry]:
        """
        Crea un campo de entrada con etiqueta.
        
        Args:
            parent: Widget padre
            label_text: Texto de la etiqueta
            icon_name: Icono para la etiqueta (opcional)
            **entry_kwargs: Argumentos para el Entry
            
        Returns:
            Tupla (Label, Entry)
        """
        frame = ttk.Frame(parent)
        
        if icon_name:
            label_text = IconHelper.text_with_icon(icon_name, label_text)
        
        label = tk.Label(frame, text=label_text)
        label.pack(side='left', padx=5)
        
        entry = tk.Entry(frame, **entry_kwargs)
        entry.pack(side='left', padx=5)
        
        return label, entry
    
    @staticmethod
    def create_combo_with_label(parent: tk.Widget, label_text: str, 
                              values: List[str], icon_name: str = None,
                              **combo_kwargs) -> Tuple[tk.Label, ttk.Combobox]:
        """
        Crea un combobox con etiqueta.
        
        Args:
            parent: Widget padre
            label_text: Texto de la etiqueta
            values: Valores del combobox
            icon_name: Icono para la etiqueta (opcional)
            **combo_kwargs: Argumentos para el Combobox
            
        Returns:
            Tupla (Label, Combobox)
        """
        if icon_name:
            label_text = IconHelper.text_with_icon(icon_name, label_text)
        
        label = tk.Label(parent, text=label_text)
        combo = ttk.Combobox(parent, values=values, state='readonly', **combo_kwargs)
        
        return label, combo
    
    @staticmethod
    def create_button_row(parent: tk.Widget, 
                         buttons: List[Dict[str, Any]]) -> List[ttk.Button]:
        """
        Crea una fila de botones.
        
        Args:
            parent: Widget padre
            buttons: Lista de configuraciones de botones
                    [{"text": "...", "icon": "...", "command": ..., ...}]
            
        Returns:
            Lista de botones creados
        """
        frame = ttk.Frame(parent)
        frame.pack(pady=5)
        
        created_buttons = []
        
        for btn_config in buttons:
            text = btn_config.get("text", "")
            icon = btn_config.get("icon")
            command = btn_config.get("command")
            
            if icon:
                text = IconHelper.text_with_icon(icon, text)
            
            # Extraer argumentos del botón
            btn_kwargs = {k: v for k, v in btn_config.items() 
                         if k not in ["text", "icon", "command"]}
            
            button = ttk.Button(frame, text=text, command=command, **btn_kwargs)
            button.pack(side='left', padx=5)
            created_buttons.append(button)
        
        return created_buttons
