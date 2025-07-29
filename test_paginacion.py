#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script de prueba para verificar la paginación

def test_paginacion():
    # Simular una lista de 15 cuentas
    cuentas_test = []
    for i in range(1, 16):
        cuentas_test.append({
            'steamid': str(i),
            'nombre': f'Cuenta {i}',
            'ruta': f'/path/{i}',
            'avatar': None
        })
    
    items_por_pagina = 10
    
    print(f"Total de cuentas: {len(cuentas_test)}")
    print(f"Items por página: {items_por_pagina}")
    
    # Calcular número de páginas
    total_paginas = max(1, (len(cuentas_test) + items_por_pagina - 1) // items_por_pagina)
    print(f"Total de páginas: {total_paginas}")
    
    # Probar cada página
    for pagina in range(1, total_paginas + 1):
        inicio = (pagina - 1) * items_por_pagina
        fin = inicio + items_por_pagina
        cuentas_pagina = cuentas_test[inicio:fin]
        
        print(f"\n--- PÁGINA {pagina} ---")
        print(f"Índices: {inicio} a {fin-1}")
        print(f"Cuentas en esta página: {len(cuentas_pagina)}")
        for cuenta in cuentas_pagina:
            print(f"  - {cuenta['nombre']} (ID: {cuenta['steamid']})")

if __name__ == "__main__":
    test_paginacion()
