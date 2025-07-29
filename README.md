# 🎮 Dota 2 Config Copier

Una aplicación de escritorio para copiar configuraciones de Dota 2 entre cuentas de Steam de manera sencilla y eficiente.

![Version](https://img.shields.io/badge/version-v1.3-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![Language](https://img.shields.io/badge/language-Python-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 📋 Descripción

**Dota 2 Config Copier** es una herramienta que permite transferir configuraciones completas de Dota 2 (controles, configuraciones de video, audio, hotkeys, etc.) desde una cuenta de Steam a otra. Ideal para usuarios que tienen múltiples cuentas o que quieren compartir su configuración optimizada.

## ✨ Características Principales

### 🔍 **Detección Automática**
- Detecta automáticamente todas las cuentas de Steam con Dota 2 instalado
- Extrae nombres de usuario y avatares de Steam
- Muestra información detallada de cada cuenta (SteamID, nombre)

### 🎯 **Interfaz Intuitiva**
- **Pestañas organizadas**: Cuentas disponibles y cuentas ignoradas
- **Iconos descriptivos**: Facilitan la identificación de funciones
- **Paginación inteligente**: Maneja eficientemente listas grandes de cuentas
- **Selección visual**: Colores distintivos para origen y destino

### 📄 **Paginación Avanzada**
- Control personalizable de elementos por página (10, 15, 20, 25, 30)
- Navegación con botones numerados
- Auto-navegación a cuentas seleccionadas
- Persistencia de preferencias de visualización

### 🚫 **Gestión de Cuentas**
- **Ignorar cuentas**: Oculta cuentas no utilizadas del listado principal
- **Restaurar cuentas**: Devuelve cuentas ignoradas cuando sea necesario
- **Persistencia**: Las preferencias se guardan automáticamente

### 💾 **Configuración Persistente**
- Recuerda última selección de origen y destino
- Guarda lista de cuentas ignoradas
- Mantiene preferencias de paginación
- Archivo JSON para configuraciones de usuario

## 🖥️ Interfaz de Usuario

### Botones Principales
- **📤 Origen**: Selecciona la cuenta fuente de la configuración
- **📥 Destino**: Selecciona la cuenta que recibirá la configuración
- **🚫 Ignorar**: Oculta la cuenta del listado principal
- **↩️ Restaurar**: Devuelve cuenta ignorada al listado
- **📋 Copiar configuración**: Ejecuta la transferencia
- **❌ Cancelar selección**: Limpia selecciones actuales

### Navegación
- **⬅️ Anterior / ➡️ Siguiente**: Navegación entre páginas
- **Botones numerados**: Acceso directo a páginas específicas
- **📄 Control de elementos**: Personaliza cuántas cuentas mostrar por página

## 🛠️ Requisitos del Sistema

- **Sistema Operativo**: Windows 7/8/10/11
- **Python**: 3.6 o superior
- **Steam**: Instalado con al menos una cuenta que tenga Dota 2
- **Librerías Python**:
  - `tkinter` (incluida con Python)
  - `Pillow` (PIL) - Para manejo de imágenes
  - `json` (incluida con Python)

## 📦 Instalación

### Opción 1: Ejecutable (Recomendado)
1. Descargar el archivo `dota_main_config.exe`
2. Colocar en cualquier carpeta
3. Ejecutar como administrador (recomendado)

### Opción 2: Código Fuente
1. Instalar Python 3.6+
2. Instalar dependencias:
   ```bash
   pip install Pillow
   ```
3. Ejecutar:
   ```bash
   python dota_main_config.py
   ```

## 🚀 Uso

### Pasos Básicos
1. **Ejecutar la aplicación**
2. **Seleccionar origen**: Hacer clic en "📤 Origen" de la cuenta que tiene la configuración deseada
3. **Seleccionar destino**: Hacer clic en "📥 Destino" de la cuenta que recibirá la configuración
4. **Copiar**: Hacer clic en "📋 Copiar configuración"
5. **Confirmar**: Aceptar la confirmación de copia

### Funciones Avanzadas

#### Gestión de Cuentas
- **Ignorar cuenta**: Usar "🚫 Ignorar" para ocultar cuentas no utilizadas
- **Restaurar cuenta**: Ir a pestaña "Cuentas Ignoradas" y usar "↩️ Restaurar"

#### Paginación
- **Cambiar elementos por página**: Usar el dropdown "📄 Mostrar"
- **Navegar**: Usar botones numerados o "⬅️ Anterior / ➡️ Siguiente"

## 📁 Estructura de Archivos

```
dota2-config-copier/
├── dota_main_config.py      # Aplicación principal
├── dota2.ico                # Icono de la aplicación
├── ultima_seleccion.json    # Configuraciones del usuario
├── README.md                # Este archivo
├── CHANGELOG.md             # Historial de cambios
└── docs/                    # Documentación adicional
    ├── ICONOS_IMPLEMENTADOS.md
    ├── PAGINACION_IMPLEMENTADA.md
    └── CAMBIOS_IMPLEMENTADOS.md
```

## ⚙️ Configuración

### Archivo `ultima_seleccion.json`
```json
{
  "origen": "steamid_origen",
  "destino": "steamid_destino",
  "cuentas_ignoradas": ["steamid1", "steamid2"],
  "items_por_pagina": 10
}
```

### Rutas por Defecto
- **Steam UserData**: `C:\Program Files (x86)\Steam\userdata`
- **Avatar Cache**: `C:\Program Files (x86)\Steam\config\avatarcache`
- **Dota 2 Config**: `[userdata]\[steamid]\570\`

## 🔒 Seguridad

- ✅ **Solo lectura/escritura**: No modifica archivos de Steam core
- ✅ **Backup automático**: Steam mantiene backups en la nube
- ✅ **Validación**: Confirma rutas antes de copiar
- ✅ **Error handling**: Manejo seguro de errores de E/O

## 🐛 Solución de Problemas

### Problemas Comunes

**No detecta cuentas:**
- Verificar que Steam esté instalado en la ruta estándar
- Asegurar que las cuentas tengan Dota 2 instalado
- Ejecutar como administrador

**Error al copiar:**
- Cerrar Steam antes de copiar
- Verificar permisos de escritura
- Comprobar espacio en disco

**No aparecen avatares:**
- Los avatares se cargan desde caché de Steam
- Algunos usuarios pueden no tener avatar

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Sadohu**
- Desarrollo y mantenimiento principal

## 🙏 Agradecimientos

- Comunidad de Dota 2 por feedback y testing
- Valve por la estructura abierta de configuraciones
- Usuarios beta por reportes de bugs y sugerencias

## 📈 Roadmap

### v1.4 (Próxima)
- [ ] Backup automático antes de copiar
- [ ] Soporte para configuraciones específicas (solo hotkeys, solo video, etc.)
- [ ] Modo portable (sin instalación)

### v1.5 (Futuro)
- [ ] Soporte para otros juegos de Steam
- [ ] Interfaz web opcional
- [ ] Sincronización automática entre cuentas

## 📞 Soporte

- **Issues**: GitHub Issues
- **Documentación**: Carpeta `docs/`
- **FAQ**: Wiki del proyecto

---

*Dota 2 Config Copier - Simplificando la gestión de configuraciones de Dota 2*
