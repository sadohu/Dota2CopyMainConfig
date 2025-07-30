# Build Configuration

Este directorio contiene los archivos de configuración para generar el ejecutable del proyecto DotaTwin.

## Archivos

- `DotaTwin_v3.0.0.spec` - Archivo de configuración de PyInstaller (ACTUAL)
- `Dota2ConfigCopier_v2.1.1.spec` - Archivo legacy (mantener para compatibilidad)

## Uso

Para generar el ejecutable, ejecuta desde la raíz del proyecto:

```bash
pyinstaller build_config/DotaTwin_v3.0.0.spec
```

## Notas

- El archivo spec está configurado para usar rutas relativas desde la raíz del proyecto
- El icono y otros assets se encuentran en `config/assets/`
- El ejecutable resultante se genera en la carpeta `dist/`
- El nuevo ejecutable se llamará `DotaTwin_v3.0.0.exe`
