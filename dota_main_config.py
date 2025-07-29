import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
import json
import re
from PIL import Image, ImageTk

STEAM_USERDATA_PATH = r"C:\Program Files (x86)\Steam\userdata"
AVATAR_CACHE_PATH = r"C:\Program Files (x86)\Steam\config\avatarcache"
CACHE_FILE = "ultima_seleccion.json"
ICON_PATH = "dota2.ico"

def encontrar_cuentas_con_dota2():
    cuentas = []
    if not os.path.exists(STEAM_USERDATA_PATH):
        return cuentas

    for carpeta in os.listdir(STEAM_USERDATA_PATH):
        user_path = os.path.join(STEAM_USERDATA_PATH, carpeta)
        dota_path = os.path.join(user_path, "570")
        config_path = os.path.join(user_path, "config", "localconfig.vdf")
        nombre = "Desconocido"
        avatar_path = None

        if os.path.exists(dota_path):
            try:
                steam3_id = int(carpeta)
                steamid64 = str(steam3_id + 76561197960265728)
                posible_avatar = os.path.join(AVATAR_CACHE_PATH, f"{steamid64}.png")
                if os.path.exists(posible_avatar):
                    avatar_path = posible_avatar
            except Exception:
                pass

            if os.path.exists(config_path):
                try:
                    with open(config_path, encoding='utf-8') as f:
                        contenido = f.read()
                        match = re.search(r'"PersonaName"\s+"([^"]+)"', contenido)
                        if match:
                            nombre = match.group(1)
                except Exception:
                    pass

            cuentas.append({
                "steamid": carpeta,
                "nombre": nombre,
                "ruta": dota_path,
                "avatar": avatar_path
            })
    return cuentas

def copiar_carpeta(origen, destino):
    try:
        for root, dirs, files in os.walk(origen):
            rel_path = os.path.relpath(root, origen)
            target_path = os.path.join(destino, rel_path)
            os.makedirs(target_path, exist_ok=True)
            for file in files:
                shutil.copy2(os.path.join(root, file), os.path.join(target_path, file))
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error copiando archivos: {e}")
        return False

def guardar_configuracion(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def cargar_configuracion():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                config = json.load(f)
                # Asegurar que existe la estructura completa
                if "cuentas_ignoradas" not in config:
                    config["cuentas_ignoradas"] = []
                if "origen" not in config:
                    config["origen"] = ""
                if "destino" not in config:
                    config["destino"] = ""
                if "items_por_pagina" not in config:
                    config["items_por_pagina"] = 10
                return config
        except (json.JSONDecodeError, KeyError):
            # Si hay error al leer, crear estructura nueva
            pass
    return {
        "origen": "",
        "destino": "",
        "cuentas_ignoradas": [],
        "items_por_pagina": 10
    }

def guardar_seleccion(origen_id, destino_id):
    config = cargar_configuracion()
    config["origen"] = origen_id
    config["destino"] = destino_id
    guardar_configuracion(config)

def cargar_seleccion():
    config = cargar_configuracion()
    return {"origen": config.get("origen", ""), "destino": config.get("destino", "")}

def ignorar_cuenta(steamid):
    config = cargar_configuracion()
    # Asegurar que existe la lista de cuentas ignoradas
    if "cuentas_ignoradas" not in config:
        config["cuentas_ignoradas"] = []
    
    if steamid not in config["cuentas_ignoradas"]:
        config["cuentas_ignoradas"].append(steamid)
        guardar_configuracion(config)

def restaurar_cuenta(steamid):
    config = cargar_configuracion()
    # Asegurar que existe la lista de cuentas ignoradas
    if "cuentas_ignoradas" not in config:
        config["cuentas_ignoradas"] = []
    
    if steamid in config["cuentas_ignoradas"]:
        config["cuentas_ignoradas"].remove(steamid)
        guardar_configuracion(config)

def obtener_cuentas_ignoradas():
    config = cargar_configuracion()
    return config.get("cuentas_ignoradas", [])

def guardar_items_por_pagina(cantidad):
    config = cargar_configuracion()
    config["items_por_pagina"] = cantidad
    guardar_configuracion(config)

def obtener_items_por_pagina():
    config = cargar_configuracion()
    return config.get("items_por_pagina", 10)

def calcular_paginas(total_items, items_por_pagina):
    """Calcula el número total de páginas"""
    return max(1, (total_items + items_por_pagina - 1) // items_por_pagina)

def obtener_items_pagina(lista, pagina_actual, items_por_pagina):
    """Obtiene los items de una página específica"""
    inicio = (pagina_actual - 1) * items_por_pagina
    fin = inicio + items_por_pagina
    return lista[inicio:fin]

def encontrar_pagina_cuenta(lista, steamid, items_por_pagina):
    """Encuentra en qué página está una cuenta específica"""
    for i, cuenta in enumerate(lista):
        if cuenta['steamid'] == steamid:
            return (i // items_por_pagina) + 1
    return 1

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Copiar Configuración de Dota 2 - By Sadohu")

        # ✅ Estilos deben ir después de crear root
        style = ttk.Style(self.root)
        style.configure("Origen.TFrame", background="#d0f0ff")
        style.configure("Destino.TFrame", background="#e0ffe0")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Ignorada.TFrame", background="#ffcccc")

        if os.path.exists(ICON_PATH):
            self.root.iconbitmap(ICON_PATH)

        self.cuentas = encontrar_cuentas_con_dota2()
        self.origen = None
        self.destino = None
        self.frames_por_id = {}
        self.frames_ignoradas_por_id = {}
        
        # Variables de paginación
        self.pagina_actual_principal = 1
        self.pagina_actual_ignoradas = 1
        self.items_por_pagina = obtener_items_por_pagina()

        self.seleccion_previa = cargar_seleccion()
        self.construir_interfaz()

    def construir_interfaz(self):
        self.avatar_refs = []  # Evitar que imágenes sean recolectadas por el GC
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña principal
        self.tab_principal = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_principal, text="Cuentas Disponibles")
        
        # Pestaña de cuentas ignoradas
        self.tab_ignoradas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ignoradas, text="Cuentas Ignoradas")
        
        self.construir_tab_principal()
        self.construir_tab_ignoradas()

    def construir_tab_principal(self):
        tk.Label(self.tab_principal, text="🎮 Cuentas Steam con Dota 2 detectadas:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Frame para controles de paginación superior
        controles_frame = ttk.Frame(self.tab_principal)
        controles_frame.pack(fill='x', padx=5, pady=5)
        
        # Control de items por página
        tk.Label(controles_frame, text="📄 Mostrar:").pack(side='left', padx=5)
        
        self.items_var = tk.StringVar(value=str(self.items_por_pagina))
        items_combo = ttk.Combobox(controles_frame, textvariable=self.items_var, 
                                  values=['10', '15', '20', '25', '30'], width=5, state='readonly')
        items_combo.pack(side='left', padx=5)
        items_combo.bind('<<ComboboxSelected>>', self.cambiar_items_por_pagina)
        
        tk.Label(controles_frame, text="cuentas por página").pack(side='left', padx=5)
        
        # Frame scrollable para las cuentas
        self.scroll_frame_principal = ttk.Frame(self.tab_principal)
        self.scroll_frame_principal.pack(fill='both', expand=True, padx=5)
        
        # Frame para navegación de páginas
        self.navegacion_frame_principal = ttk.Frame(self.tab_principal)
        self.navegacion_frame_principal.pack(fill='x', padx=5, pady=5)
        
        self.actualizar_contenido_principal(forzar_navegacion_seleccion=False)

        self.status_label = tk.Label(self.tab_principal, text="Selecciona origen y destino", font=("Arial", 10), fg="blue")
        self.status_label.pack(pady=10)

        botones_frame = ttk.Frame(self.tab_principal)
        botones_frame.pack(pady=5)

        self.btn_cancelar = ttk.Button(botones_frame, text="❌ Cancelar selección", command=self.cancelar_seleccion)
        self.btn_cancelar.pack(side='left', padx=5)

        self.btn_copiar = ttk.Button(botones_frame, text="📋 Copiar configuración", command=self.ejecutar_copia, state='disabled')
        self.btn_copiar.pack(side='left', padx=5)

        self.restaurar_seleccion()

    def construir_tab_ignoradas(self):
        tk.Label(self.tab_ignoradas, text="🔕 Cuentas ignoradas:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Frame scrollable para las cuentas ignoradas
        self.scroll_frame_ignoradas = ttk.Frame(self.tab_ignoradas)
        self.scroll_frame_ignoradas.pack(fill='both', expand=True, padx=5)
        
        # Frame para navegación de páginas ignoradas
        self.navegacion_frame_ignoradas = ttk.Frame(self.tab_ignoradas)
        self.navegacion_frame_ignoradas.pack(fill='x', padx=5, pady=5)
        
        self.actualizar_tab_ignoradas()

    def actualizar_tab_ignoradas(self):
        # Limpiar frame de cuentas ignoradas
        for widget in self.scroll_frame_ignoradas.winfo_children():
            widget.destroy()
        self.frames_ignoradas_por_id.clear()
        
        cuentas_ignoradas_ids = obtener_cuentas_ignoradas()
        cuentas_ignoradas = [cuenta for cuenta in self.cuentas if cuenta['steamid'] in cuentas_ignoradas_ids]
        
        if not cuentas_ignoradas:
            tk.Label(self.scroll_frame_ignoradas, text="No hay cuentas ignoradas", font=("Arial", 10), fg="gray").pack(pady=20)
            # Limpiar navegación
            for widget in self.navegacion_frame_ignoradas.winfo_children():
                widget.destroy()
            return

        # Obtener cuentas de la página actual
        cuentas_pagina = obtener_items_pagina(cuentas_ignoradas, self.pagina_actual_ignoradas, self.items_por_pagina)

        for cuenta in cuentas_pagina:
            self.crear_frame_cuenta_ignorada(cuenta)
            
        self.actualizar_navegacion_ignoradas(len(cuentas_ignoradas))

    def crear_frame_cuenta_ignorada(self, cuenta):
        frame = ttk.Frame(self.scroll_frame_ignoradas, padding=5)
        frame.pack(fill='x', padx=5, pady=3)

        # Crear un avatar
        if cuenta['avatar'] and os.path.exists(cuenta['avatar']):
            avatar_img = Image.open(cuenta['avatar']).resize((32, 32))
        else:
            avatar_img = Image.new("RGB", (32, 32), (64, 64, 64))
        avatar = ImageTk.PhotoImage(avatar_img)
        self.avatar_refs.append(avatar)

        img_label = tk.Label(frame, image=avatar)
        img_label.grid(row=0, column=0, padx=5)

        info = f"{cuenta['nombre']} (SteamID: {cuenta['steamid']})"
        label = tk.Label(frame, text=info, anchor='w')
        label.grid(row=0, column=1, sticky='w', padx=10)
        
        btn_restaurar = ttk.Button(frame, text="↩️ Restaurar", command=lambda c=cuenta: self.restaurar_cuenta_ui(c))
        btn_restaurar.grid(row=0, column=2, padx=5)

        frame.columnconfigure(1, weight=1)  # Expandir la columna del nombre

        self.frames_ignoradas_por_id[cuenta["steamid"]] = frame

    def actualizar_navegacion_ignoradas(self, total_cuentas):
        # Limpiar navegación actual
        for widget in self.navegacion_frame_ignoradas.winfo_children():
            widget.destroy()
            
        if total_cuentas == 0:
            return
            
        total_paginas = calcular_paginas(total_cuentas, self.items_por_pagina)
        
        if total_paginas <= 1:
            return
            
        # Botón anterior
        if self.pagina_actual_ignoradas > 1:
            btn_anterior = ttk.Button(self.navegacion_frame_ignoradas, text="⬅️ Anterior", 
                                    command=lambda: self.cambiar_pagina_ignoradas(self.pagina_actual_ignoradas - 1))
            btn_anterior.pack(side='left', padx=2)
        
        # Botones de páginas
        inicio = max(1, self.pagina_actual_ignoradas - 2)
        fin = min(total_paginas + 1, inicio + 5)
        
        for pagina in range(inicio, fin):
            if pagina == self.pagina_actual_ignoradas:
                btn = tk.Label(self.navegacion_frame_ignoradas, text=str(pagina), 
                              bg='lightblue', width=3, relief='raised')
            else:
                btn = ttk.Button(self.navegacion_frame_ignoradas, text=str(pagina), width=3,
                               command=lambda p=pagina: self.cambiar_pagina_ignoradas(p))
            btn.pack(side='left', padx=1)
        
        # Botón siguiente
        if self.pagina_actual_ignoradas < total_paginas:
            btn_siguiente = ttk.Button(self.navegacion_frame_ignoradas, text="Siguiente ➡️", 
                                     command=lambda: self.cambiar_pagina_ignoradas(self.pagina_actual_ignoradas + 1))
            btn_siguiente.pack(side='left', padx=2)
        
        # Info de página
        info_label = tk.Label(self.navegacion_frame_ignoradas, 
                             text=f"Página {self.pagina_actual_ignoradas} de {total_paginas} ({total_cuentas} cuentas)")
        info_label.pack(side='right', padx=10)

    def cambiar_pagina_ignoradas(self, nueva_pagina):
        self.pagina_actual_ignoradas = nueva_pagina
        self.actualizar_tab_ignoradas()

    def cambiar_items_por_pagina(self, event=None):
        self.items_por_pagina = int(self.items_var.get())
        guardar_items_por_pagina(self.items_por_pagina)
        
        # Ajustar páginas actuales si es necesario
        cuentas_ignoradas = obtener_cuentas_ignoradas()
        cuentas_visibles = [cuenta for cuenta in self.cuentas if cuenta['steamid'] not in cuentas_ignoradas]
        cuentas_ignoradas_list = [cuenta for cuenta in self.cuentas if cuenta['steamid'] in cuentas_ignoradas]
        
        max_pagina_principal = calcular_paginas(len(cuentas_visibles), self.items_por_pagina)
        max_pagina_ignoradas = calcular_paginas(len(cuentas_ignoradas_list), self.items_por_pagina)
        
        if self.pagina_actual_principal > max_pagina_principal:
            self.pagina_actual_principal = max_pagina_principal
        if self.pagina_actual_ignoradas > max_pagina_ignoradas:
            self.pagina_actual_ignoradas = max_pagina_ignoradas
            
        self.actualizar_contenido_principal()
        self.actualizar_tab_ignoradas()

    def actualizar_contenido_principal(self, forzar_navegacion_seleccion=False):
        # Limpiar contenido actual
        for widget in self.scroll_frame_principal.winfo_children():
            widget.destroy()
        self.frames_por_id.clear()
        
        cuentas_ignoradas = obtener_cuentas_ignoradas()
        cuentas_visibles = [cuenta for cuenta in self.cuentas if cuenta['steamid'] not in cuentas_ignoradas]
        
        # Solo navegar automáticamente si se fuerza (restaurar selección) o si no hay navegación manual
        if forzar_navegacion_seleccion:
            if self.origen and self.origen['steamid'] not in cuentas_ignoradas:
                pagina_origen = encontrar_pagina_cuenta(cuentas_visibles, self.origen['steamid'], self.items_por_pagina)
                self.pagina_actual_principal = pagina_origen
            elif self.destino and self.destino['steamid'] not in cuentas_ignoradas:
                pagina_destino = encontrar_pagina_cuenta(cuentas_visibles, self.destino['steamid'], self.items_por_pagina)
                self.pagina_actual_principal = pagina_destino
        
        # Asegurar que la página actual esté dentro de los límites
        total_paginas = calcular_paginas(len(cuentas_visibles), self.items_por_pagina)
        if self.pagina_actual_principal > total_paginas:
            self.pagina_actual_principal = total_paginas
        if self.pagina_actual_principal < 1:
            self.pagina_actual_principal = 1
        
        # Obtener cuentas de la página actual
        cuentas_pagina = obtener_items_pagina(cuentas_visibles, self.pagina_actual_principal, self.items_por_pagina)
        
        for cuenta in cuentas_pagina:
            self.crear_frame_cuenta_principal(cuenta)
        
        self.actualizar_navegacion_principal(len(cuentas_visibles))

    def crear_frame_cuenta_principal(self, cuenta):
        frame = ttk.Frame(self.scroll_frame_principal, padding=5)
        frame.pack(fill='x', padx=5, pady=3)

        # Crear un avatar
        if cuenta['avatar'] and os.path.exists(cuenta['avatar']):
            avatar_img = Image.open(cuenta['avatar']).resize((32, 32))
        else:
            avatar_img = Image.new("RGB", (32, 32), (64, 64, 64))
        avatar = ImageTk.PhotoImage(avatar_img)
        self.avatar_refs.append(avatar)

        img_label = tk.Label(frame, image=avatar)
        img_label.grid(row=0, column=0, padx=5)

        info = f"{cuenta['nombre']} (SteamID: {cuenta['steamid']})"
        label = tk.Label(frame, text=info, anchor='w')
        label.grid(row=0, column=1, sticky='w', padx=10)

        btn_origen = ttk.Button(frame, text="📤 Origen", command=lambda c=cuenta: self.set_origen(c))
        btn_origen.grid(row=0, column=2, padx=5)

        btn_destino = ttk.Button(frame, text="📥 Destino", command=lambda c=cuenta: self.set_destino(c))
        btn_destino.grid(row=0, column=3, padx=5)
        
        btn_ignorar = ttk.Button(frame, text="🚫 Ignorar", command=lambda c=cuenta: self.ignorar_cuenta_ui(c))
        btn_ignorar.grid(row=0, column=4, padx=5)

        frame.columnconfigure(1, weight=1)  # Expandir la columna del nombre

        self.frames_por_id[cuenta["steamid"]] = (frame, btn_origen, btn_destino)

    def actualizar_navegacion_principal(self, total_cuentas):
        # Limpiar navegación actual
        for widget in self.navegacion_frame_principal.winfo_children():
            widget.destroy()
            
        if total_cuentas == 0:
            return
            
        total_paginas = calcular_paginas(total_cuentas, self.items_por_pagina)
        
        if total_paginas <= 1:
            return
            
        # Botón anterior
        if self.pagina_actual_principal > 1:
            btn_anterior = ttk.Button(self.navegacion_frame_principal, text="⬅️ Anterior", 
                                    command=lambda: self.cambiar_pagina_principal(self.pagina_actual_principal - 1))
            btn_anterior.pack(side='left', padx=2)
        
        # Botones de páginas
        inicio = max(1, self.pagina_actual_principal - 2)
        fin = min(total_paginas + 1, inicio + 5)
        
        for pagina in range(inicio, fin):
            if pagina == self.pagina_actual_principal:
                btn = tk.Label(self.navegacion_frame_principal, text=str(pagina), 
                              bg='lightblue', width=3, relief='raised')
            else:
                btn = ttk.Button(self.navegacion_frame_principal, text=str(pagina), width=3,
                               command=lambda p=pagina: self.cambiar_pagina_principal(p))
            btn.pack(side='left', padx=1)
        
        # Botón siguiente
        if self.pagina_actual_principal < total_paginas:
            btn_siguiente = ttk.Button(self.navegacion_frame_principal, text="Siguiente ➡️", 
                                     command=lambda: self.cambiar_pagina_principal(self.pagina_actual_principal + 1))
            btn_siguiente.pack(side='left', padx=2)
        
        # Info de página
        info_label = tk.Label(self.navegacion_frame_principal, 
                             text=f"Página {self.pagina_actual_principal} de {total_paginas} ({total_cuentas} cuentas)")
        info_label.pack(side='right', padx=10)

    def cambiar_pagina_principal(self, nueva_pagina):
        self.pagina_actual_principal = nueva_pagina
        self.actualizar_contenido_principal()
        self.actualizar_estado()

    def ignorar_cuenta_ui(self, cuenta):
        confirm = messagebox.askyesno("Confirmar", f"¿Deseas ignorar la cuenta '{cuenta['nombre']}'?\n\nPodrás restaurarla desde la pestaña 'Cuentas Ignoradas'.")
        if confirm:
            ignorar_cuenta(cuenta['steamid'])
            # Si la cuenta ignorada era origen o destino, limpiar selección
            if self.origen and self.origen['steamid'] == cuenta['steamid']:
                self.origen = None
            if self.destino and self.destino['steamid'] == cuenta['steamid']:
                self.destino = None
            self.reconstruir_tabs()

    def restaurar_cuenta_ui(self, cuenta):
        restaurar_cuenta(cuenta['steamid'])
        self.reconstruir_tabs()

    def reconstruir_tabs(self):
        # Guardar página actual antes de reconstruir
        pagina_anterior = self.pagina_actual_principal
        
        # Actualizar contenido
        self.actualizar_contenido_principal(forzar_navegacion_seleccion=False)
        self.actualizar_tab_ignoradas()
        
        # Intentar mantener la página anterior si es válida
        cuentas_ignoradas = obtener_cuentas_ignoradas()
        cuentas_visibles = [cuenta for cuenta in self.cuentas if cuenta['steamid'] not in cuentas_ignoradas]
        total_paginas = calcular_paginas(len(cuentas_visibles), self.items_por_pagina)
        
        if pagina_anterior <= total_paginas:
            self.pagina_actual_principal = pagina_anterior
            self.actualizar_contenido_principal(forzar_navegacion_seleccion=False)
        else:
            self.pagina_actual_principal = 1
            self.actualizar_contenido_principal(forzar_navegacion_seleccion=False)
        
        # Actualizar estado
        self.actualizar_estado()

    def set_origen(self, cuenta):
        self.origen = cuenta
        self.actualizar_estado()

    def set_destino(self, cuenta):
        self.destino = cuenta
        self.actualizar_estado()

    def cancelar_seleccion(self):
        self.origen = None
        self.destino = None
        self.actualizar_estado()

    def actualizar_estado(self):
        # Solo actualizar cuentas que están visible (no ignoradas)
        cuentas_ignoradas = obtener_cuentas_ignoradas()
        cuentas_visibles = [cuenta for cuenta in self.cuentas if cuenta['steamid'] not in cuentas_ignoradas]
        
        for cuenta in cuentas_visibles:
            if cuenta["steamid"] in self.frames_por_id:
                frame, btn_o, btn_d = self.frames_por_id[cuenta["steamid"]]
                frame.config(style="TFrame")
                btn_o.state(["!disabled"])
                btn_d.state(["!disabled"])
                if self.origen and cuenta["steamid"] == self.origen["steamid"]:
                    frame.config(style="Origen.TFrame")
                if self.destino and cuenta["steamid"] == self.destino["steamid"]:
                    frame.config(style="Destino.TFrame")

        if self.origen and self.destino:
            if self.origen['steamid'] == self.destino['steamid']:
                self.status_label.config(text="Origen y destino no pueden ser iguales.", fg="red")
                self.btn_copiar.config(state='disabled')
            else:
                self.status_label.config(
                    text=f"Listo para copiar de '{self.origen['nombre']}' a '{self.destino['nombre']}'", fg="green"
                )
                self.btn_copiar.config(state='normal')
        else:
            self.status_label.config(text="Selecciona origen y destino", fg="blue")
            self.btn_copiar.config(state='disabled')

    def ejecutar_copia(self):
        confirm = messagebox.askyesno("Confirmar", f"¿Deseas copiar la configuración de:\n\n{self.origen['nombre']} → {self.destino['nombre']} ?")
        if confirm:
            if copiar_carpeta(self.origen['ruta'], self.destino['ruta']):
                guardar_seleccion(self.origen['steamid'], self.destino['steamid'])
                messagebox.showinfo("Éxito", "La configuración fue copiada con éxito.")

    def restaurar_seleccion(self):
        seleccion = self.seleccion_previa
        
        # Obtener listas de cuentas
        cuentas_ignoradas = obtener_cuentas_ignoradas()
        cuentas_visibles = [cuenta for cuenta in self.cuentas if cuenta['steamid'] not in cuentas_ignoradas]
        
        for cuenta in self.cuentas:
            if cuenta["steamid"] == seleccion.get("origen"):
                self.origen = cuenta
                # Si origen está en cuentas visibles, navegar a su página
                if cuenta['steamid'] not in cuentas_ignoradas:
                    pagina_origen = encontrar_pagina_cuenta(cuentas_visibles, cuenta['steamid'], self.items_por_pagina)
                    self.pagina_actual_principal = pagina_origen
                    
            if cuenta["steamid"] == seleccion.get("destino"):
                self.destino = cuenta
                # Si destino está en cuentas visibles y no se navegó por origen, navegar a su página
                if cuenta['steamid'] not in cuentas_ignoradas and not self.origen:
                    pagina_destino = encontrar_pagina_cuenta(cuentas_visibles, cuenta['steamid'], self.items_por_pagina)
                    self.pagina_actual_principal = pagina_destino
        
        # Actualizar contenido con las páginas correctas
        self.actualizar_contenido_principal(forzar_navegacion_seleccion=True)
        self.actualizar_estado()

# Ejecutar app
root = tk.Tk()
app = App(root)
root.mainloop()
