#!/usr/bin/env python3
"""
Script de prueba para el nuevo sistema de copia completa.
"""

import os
import shutil
import logging
from pathlib import Path

# Configurar logging para debugging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_full_copy(steam_path: str, origen_id: str, destino_id: str):
    """Prueba la copia completa entre dos cuentas."""
    
    # Rutas de las cuentas
    origen_path = Path(steam_path) / "userdata" / origen_id / "570" / "local" / "cfg"
    destino_path = Path(steam_path) / "userdata" / destino_id / "570" / "local" / "cfg"
    
    # Verificar que el origen existe
    if not origen_path.exists():
        logger.error(f"La carpeta de origen no existe: {origen_path}")
        return False
    
    logger.info(f"Origen: {origen_path}")
    logger.info(f"Destino: {destino_path}")
    
    # Contar archivos en origen
    origen_files = []
    for root, dirs, files in os.walk(origen_path):
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(origen_path)
            origen_files.append(str(rel_path))
    
    logger.info(f"Archivos en origen ({len(origen_files)}):")
    for file in sorted(origen_files):
        logger.info(f"  {file}")
    
    # Crear backup del destino si existe
    backup_path = None
    if destino_path.exists():
        backup_path = destino_path.parent / "cfg_backup_test"
        if backup_path.exists():
            shutil.rmtree(backup_path)
        shutil.copytree(destino_path, backup_path)
        logger.info(f"Backup creado en: {backup_path}")
        
        # Contar archivos en destino antes
        destino_files_before = []
        for root, dirs, files in os.walk(destino_path):
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(destino_path)
                destino_files_before.append(str(rel_path))
        
        logger.info(f"Archivos en destino ANTES ({len(destino_files_before)}):")
        for file in sorted(destino_files_before):
            logger.info(f"  {file}")
    
    try:
        # Realizar la copia completa
        logger.info("=== INICIANDO COPIA COMPLETA ===")
        
        # Eliminar destino si existe
        if destino_path.exists():
            shutil.rmtree(destino_path)
            logger.info("Destino eliminado")
        
        # Copiar toda la carpeta
        shutil.copytree(origen_path, destino_path)
        logger.info("Copia completa realizada")
        
        # Verificar resultado
        destino_files_after = []
        for root, dirs, files in os.walk(destino_path):
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(destino_path)
                destino_files_after.append(str(rel_path))
        
        logger.info(f"Archivos en destino DESPUÉS ({len(destino_files_after)}):")
        for file in sorted(destino_files_after):
            logger.info(f"  {file}")
        
        # Comparar
        if set(origen_files) == set(destino_files_after):
            logger.info("✅ ÉXITO: Todos los archivos se copiaron correctamente")
            logger.info(f"Total de archivos copiados: {len(destino_files_after)}")
            return True
        else:
            logger.error("❌ ERROR: Los archivos no coinciden")
            logger.error(f"Faltantes: {set(origen_files) - set(destino_files_after)}")
            logger.error(f"Extras: {set(destino_files_after) - set(origen_files)}")
            return False
            
    except Exception as e:
        logger.error(f"Error durante la copia: {e}")
        
        # Restaurar backup si existe
        if backup_path and backup_path.exists():
            if destino_path.exists():
                shutil.rmtree(destino_path)
            shutil.copytree(backup_path, destino_path)
            logger.info("Backup restaurado debido al error")
        
        return False
    
    finally:
        # Limpiar backup
        if backup_path and backup_path.exists():
            shutil.rmtree(backup_path)
            logger.info("Backup temporal eliminado")

def main():
    """Test con cuentas reales."""
    steam_path = r"C:\Program Files (x86)\Steam"
    
    # Test con las cuentas que están siendo usadas según los logs
    origen_id = "1770091162"
    destino_id = "172779231"
    
    logger.info("=== PRUEBA DE COPIA COMPLETA v2.1.2 ===")
    logger.info(f"Steam path: {steam_path}")
    logger.info(f"Origen: {origen_id}")
    logger.info(f"Destino: {destino_id}")
    
    success = test_full_copy(steam_path, origen_id, destino_id)
    
    if success:
        logger.info("🎉 PRUEBA EXITOSA - El nuevo sistema de copia funciona correctamente")
    else:
        logger.error("💥 PRUEBA FALLIDA - Revisar implementación")

if __name__ == "__main__":
    main()
