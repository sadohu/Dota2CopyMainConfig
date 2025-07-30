# 🎮 DotaTwin v3.1.0 - Distribución y Instalación

**Desarrollado por Sadohu** | 29 de julio de 2025

## ✨ ¡Nuevo! DotaTwin v3.1.0

**Twin your Dota experience** - DotaTwin permite **duplicar configuraciones de Dota 2** entre cuentas de Steam, creando "gemelos digitales" de tu setup perfecto.

### 🆕 Novedades en v3.1.0
- **🎉 Versión Portable**: Nueva opción sin alertas de Windows SmartScreen
- **📦 Doble distribución**: Ejecutable PyInstaller + Portable Python
- **🛡️ Documentación de seguridad**: Guía completa sobre alertas de Windows
- **🔧 Build automatizado**: Script para crear portable automáticamente

## 📥 Opciones de Descarga

### 🆕 Opción 1: Portable (Recomendado - Sin alertas)
- **Archivo**: `DotaTwin_v3.1.0_Portable.zip` (21 MB)
- **Ventajas**: Sin alertas Windows SmartScreen, código auditable
- **Instalación**: Extraer ZIP y ejecutar `run.bat`
- **Requisitos**: Windows 7+ (Python embebido incluido)

### Opción 2: Ejecutable Standalone  
- **Archivo**: `DotaTwin_v3.1.0.exe` (47 MB)
- **Ventajas**: Un solo archivo, ejecución inmediata
- **Nota**: Puede mostrar alerta Windows SmartScreen (aceptar para continuar)
- **Requisitos**: Windows 10+ (64-bit)

### Opción 3: Código Fuente
- **Método**: Clonar repositorio GitHub
- **Comando**: `git clone https://github.com/sadohu/DotaTwin.git`
- **Ejecución**: `python main.py`
- **Requisitos**: Python 3.8+ con tkinter

## 🛡️ Sobre las Alertas de Windows

### ¿Por qué aparece la alerta?
Windows SmartScreen puede mostrar alertas porque:
- DotaTwin no tiene firma digital (certificado cuesta ~$300/año)
- Es una aplicación nueva sin "reputación" establecida
- Windows es muy cauteloso con software independiente

### ¿Es seguro DotaTwin?
**¡SÍ, absolutamente!** DotaTwin es 100% seguro:
- ✅ **Código abierto** en GitHub
- ✅ **Sin malware** - solo copia archivos .vcfg
- ✅ **Sin conexión a internet**
- ✅ **Sin modificaciones del sistema**

### Alternativas si prefieres evitar la alerta:
1. **🆕 Usar versión portable** - Sin alertas
2. **Ejecutar desde código fuente** - Máxima transparencia
3. **Revisar código en GitHub** - Verificación manual

## 🚀 Instalación Detallada

### Para Versión Portable:
1. Descargar `DotaTwin_v3.1.0_Portable.zip`
2. Extraer en cualquier carpeta
3. Doble clic en `run.bat`
4. ¡Listo! Sin alertas ni instalación

### Para Ejecutable:
1. Descargar `DotaTwin_v3.1.0.exe`
2. Si aparece alerta: "Más información" → "Ejecutar de todas formas"
3. Colocar en cualquier carpeta y ejecutar

### Para Código Fuente:
```bash
git clone https://github.com/sadohu/DotaTwin.git
cd DotaTwin
pip install -r requirements.txt
python main.py
```

## ✨ Características de v3.1.0

### 🔧 Funcionalidades Principales
- ✅ **Detección automática** de cuentas Steam con Dota 2
- ✅ **Copia segura** de configuraciones entre cuentas
- ✅ **Respaldo automático** antes de cada operación
- ✅ **Sistema de ignorar cuentas** para ocultar cuentas no deseadas
- ✅ **Interfaz intuitiva** con navegación por pestañas
- ✅ **Logging detallado** para troubleshooting
- ✅ **🆕 Versión portable** sin alertas de Windows

### 🎯 Arquitectura v3.1.0
- **Base modular sólida** y mantenible
- **Configuración avanzada** de Steam
- **Layout responsive** adaptable
- **Sistema de build automatizado**

## 🎮 Uso Básico

### Primer Uso
1. **Ejecutar aplicación** (run.bat o .exe)
2. **Detección automática** de cuentas Steam
3. **Seleccionar origen** (📤) y **destino** (📥)
4. **Copiar configuración** con un clic

### Gestión de Cuentas
- **Ignorar**: Usar 🚫 para ocultar cuentas no deseadas
- **Restaurar**: Pestaña "Cuentas Ignoradas" → ↩️
- **Paginación**: Cambiar elementos mostrados por página

## 🔧 Resolución de Problemas

### Problema: "tkinter no disponible" (Portable)
**Solución**: Usar Python del sistema: `python DotaTwin_launcher.py`

### Problema: Archivos no encontrados
**Solución**: Verificar que Steam esté instalado y Dota 2 configurado

### Problema: Error de permisos
**Solución**: Ejecutar como administrador

## 📞 Soporte y Contacto

- **GitHub**: https://github.com/sadohu/DotaTwin
- **Issues**: Reportar problemas en GitHub Issues
- **Documentación**: Ver README.md completo

## 📄 Licencia

MIT License - Software libre y gratuito

---

**🎮 ¡Disfruta twinning tu experiencia Dota con DotaTwin v3.1.0!**
