import json
import os

CACHE_FILE = "ultima_seleccion.json"

def migrar_json():
    """Migra el archivo JSON al nuevo formato si es necesario"""
    if os.path.exists(CACHE_FILE):
        print("Verificando archivo JSON existente...")
        try:
            with open(CACHE_FILE, "r") as f:
                config = json.load(f)
            
            print(f"Contenido actual: {config}")
            
            # Verificar si necesita migración
            necesita_migracion = False
            if "cuentas_ignoradas" not in config:
                config["cuentas_ignoradas"] = []
                necesita_migracion = True
                print("✓ Agregando campo 'cuentas_ignoradas'")
            
            if "origen" not in config:
                config["origen"] = ""
                necesita_migracion = True
                print("✓ Agregando campo 'origen'")
                
            if "destino" not in config:
                config["destino"] = ""
                necesita_migracion = True
                print("✓ Agregando campo 'destino'")
            
            if necesita_migracion:
                # Hacer backup del archivo original
                import shutil
                shutil.copy(CACHE_FILE, f"{CACHE_FILE}.backup")
                print(f"✓ Backup creado: {CACHE_FILE}.backup")
                
                # Guardar la nueva estructura
                with open(CACHE_FILE, "w") as f:
                    json.dump(config, f, indent=2)
                print("✓ Archivo migrado exitosamente")
                print(f"Nuevo contenido: {config}")
            else:
                print("✓ El archivo ya tiene el formato correcto")
                
        except json.JSONDecodeError as e:
            print(f"Error al leer JSON: {e}")
            print("Creando nuevo archivo con estructura correcta...")
            config = {
                "origen": "",
                "destino": "",
                "cuentas_ignoradas": []
            }
            with open(CACHE_FILE, "w") as f:
                json.dump(config, f, indent=2)
            print("✓ Nuevo archivo creado")
    else:
        print("No existe archivo JSON, se creará automáticamente al usar el programa")

if __name__ == "__main__":
    migrar_json()
