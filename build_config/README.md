# Build Configuration

Este directorio contiene los archivos de configuración para generar el ejecutable del proyecto.

## Archivos

- `Dota2ConfigCopier_v2.1.1.spec` - Archivo de configuración de PyInstaller

## Uso

Para generar el ejecutable, ejecuta desde la raíz del proyecto:

```bash
pyinstaller build_config/Dota2ConfigCopier_v2.1.1.spec
```

## Notas

- El archivo spec está configurado para usar rutas relativas desde la raíz del proyecto
- El icono y otros assets se encuentran en `config/assets/`
- El ejecutable resultante se genera en la carpeta `dist/`
