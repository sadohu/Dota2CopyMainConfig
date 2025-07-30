# Build Configuration

Este directorio contiene los archivos de configuración para generar el ejecutable del proyecto DotaTwin.

## Archivos

- `DotaTwin_v3.0.0.spec` - Archivo de configuración de PyInstaller (ACTUAL)
- `Dota2ConfigCopier_v2.1.1.spec` - Archivo legacy (mantener para compatibilidad)

## Uso

Para generar el ejecutable, ejecuta desde el directorio `build_config`:

```bash
cd build_config
pyinstaller DotaTwin_v3.0.0.spec --clean
```

## Notas Importantes

### ✅ Corregido en v3.0.0:
- **GitIgnore**: Removido `*.spec` del .gitignore para incluir archivos de configuración
- **Rutas de Icono**: Implementada detección automática de entorno (desarrollo vs. empaquetado)
- **Assets**: El icono se incluye correctamente usando `sys._MEIPASS` en ejecutables
- **Función `_get_resource_path()`**: Nueva función para resolver rutas dinámicamente

### 🔧 Mejoras técnicas:
- **Detección de entorno**: `getattr(sys, 'frozen', False)` para detectar PyInstaller
- **Rutas dinámicas**: `sys._MEIPASS` para recursos en ejecutables empaquetados
- **Compatibilidad**: Funciona tanto en desarrollo como en producción

### 📁 Estructura:
- El archivo spec está configurado para usar rutas relativas desde `build_config/`
- El icono se encuentra en `../config/assets/dota2.ico`
- El ejecutable resultante se genera en la carpeta `dist/`
- El nuevo ejecutable se llamará `DotaTwin_v3.0.0.exe`

### 🔧 Características del Build:
- Optimización nivel 2
- Compresión UPX habilitada
- Sin ventana de consola
- Icono integrado en el ejecutable
