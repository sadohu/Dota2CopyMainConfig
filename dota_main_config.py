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

def guardar_seleccion(origen_id, destino_id):
    with open(CACHE_FILE, "w") as f:
        json.dump({"origen": origen_id, "destino": destino_id}, f)

def cargar_seleccion():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Copiar Configuración de Dota 2")

        # ✅ Estilos deben ir después de crear root
        style = ttk.Style(self.root)
        style.configure("Origen.TFrame", background="#d0f0ff")
        style.configure("Destino.TFrame", background="#e0ffe0")
        style.configure("TFrame", background="#f0f0f0")

        if os.path.exists(ICON_PATH):
            self.root.iconbitmap(ICON_PATH)

        self.cuentas = encontrar_cuentas_con_dota2()
        self.origen = None
        self.destino = None
        self.frames_por_id = {}

        self.seleccion_previa = cargar_seleccion()
        self.construir_interfaz()

    def construir_interfaz(self):
        self.avatar_refs = []  # Evitar que imágenes sean recolectadas por el GC
        tk.Label(self.root, text="Cuentas Steam con Dota 2 detectadas:", font=("Arial", 12, "bold")).pack(pady=10)

        for cuenta in self.cuentas:
            frame = ttk.Frame(self.root, padding=5)
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

            btn_origen = ttk.Button(frame, text="Origen", command=lambda c=cuenta: self.set_origen(c))
            btn_origen.grid(row=0, column=2, padx=5)

            btn_destino = ttk.Button(frame, text="Destino", command=lambda c=cuenta: self.set_destino(c))
            btn_destino.grid(row=0, column=3, padx=5)

            frame.columnconfigure(1, weight=1)  # Expandir la columna del nombre

            self.frames_por_id[cuenta["steamid"]] = (frame, btn_origen, btn_destino)

        self.status_label = tk.Label(self.root, text="Selecciona origen y destino", font=("Arial", 10), fg="blue")
        self.status_label.pack(pady=10)

        self.btn_cancelar = ttk.Button(self.root, text="Cancelar selección", command=self.cancelar_seleccion)
        self.btn_cancelar.pack(pady=5)

        self.btn_copiar = ttk.Button(self.root, text="Copiar configuración", command=self.ejecutar_copia, state='disabled')
        self.btn_copiar.pack(pady=10)

        self.restaurar_seleccion()

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
        for cuenta in self.cuentas:
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
        for cuenta in self.cuentas:
            if cuenta["steamid"] == seleccion.get("origen"):
                self.origen = cuenta
            if cuenta["steamid"] == seleccion.get("destino"):
                self.destino = cuenta
        self.actualizar_estado()

# Ejecutar app
root = tk.Tk()
app = App(root)
root.mainloop()
