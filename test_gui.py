import tkinter as tk
from tkinter import ttk

# Prueba simple de la interfaz
root = tk.Tk()
root.title("Test")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Tab 1")

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Tab 2")

tk.Label(tab1, text="Contenido de Tab 1").pack(pady=20)
tk.Label(tab2, text="Contenido de Tab 2").pack(pady=20)

root.mainloop()
