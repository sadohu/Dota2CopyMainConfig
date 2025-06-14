import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
import re

STEAM_USERDATA_PATH = r"C:\Program Files (x86)\Steam\userdata"

def encontrar_cuentas_con_dota2():
    cuentas = []
    if not os.path.exists(STEAM_USERDATA_PATH):
        return cuentas

    for carpeta in os.listdir(STEAM_USERDATA_PATH):
        user_path = os.path.join(STEAM_USERDATA_PATH, carpeta)
        dota_path = os.path.join(user_path, "570")
        config_path = os.path.join(user_path, "config", "localconfig.vdf")
        nombre = "Desconocido"

        if os.path.exists(dota_path):
            # Intentar leer el nombre del usuario
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
                "ruta": dota_path
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

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Copiar Configuración de Dota 2")
        self.cuentas = encontrar_cuentas_con_dota2()
        self.origen = None
        self.destino = None
        self.construir_interfaz()

    def construir_interfaz(self):
        tk.Label(self.root, text="Cuentas Steam con Dota 2 detectadas:", font=("Arial", 12, "bold")).pack(pady=10)

        for cuenta in self.cuentas:
            frame = ttk.Frame(self.root, padding=5)
            frame.pack(fill='x')

            info = f"{cuenta['nombre']}  (SteamID: {cuenta['steamid']})"
            label = tk.Label(frame, text=info)
            label.pack(side='left', padx=5)

            btn_origen = ttk.Button(frame, text="Usar como ORIGEN", command=lambda c=cuenta: self.set_origen(c))
            btn_origen.pack(side='right', padx=5)

            btn_destino = ttk.Button(frame, text="Usar como DESTINO", command=lambda c=cuenta: self.set_destino(c))
            btn_destino.pack(side='right')

        self.status_label = tk.Label(self.root, text="Selecciona origen y destino", font=("Arial", 10), fg="blue")
        self.status_label.pack(pady=10)

        self.btn_copiar = ttk.Button(self.root, text="Copiar configuración", command=self.ejecutar_copia, state='disabled')
        self.btn_copiar.pack(pady=10)

    def set_origen(self, cuenta):
        self.origen = cuenta
        self.actualizar_estado()

    def set_destino(self, cuenta):
        self.destino = cuenta
        self.actualizar_estado()

    def actualizar_estado(self):
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
            origen_path = self.origen['ruta']
            destino_path = self.destino['ruta']
            if copiar_carpeta(origen_path, destino_path):
                messagebox.showinfo("Éxito", "La configuración fue copiada con éxito.")
            else:
                messagebox.showerror("Error", "Ocurrió un problema al copiar.")

# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
