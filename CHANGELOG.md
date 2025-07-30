# 📝 CHANGELOG

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [v3.1.0] - 2025-07-29 🚀 PREPARACIÓN PARA GITHUB RELEASES

### 🌐 **DISTRIBUCIÓN Y SEGURIDAD**
- **GitHub Releases**: Preparación completa para distribución oficial a través de GitHub
- **Documentación de seguridad**: Sección completa en README sobre alertas de Windows SmartScreen
- **Transparencia total**: Explicación detallada de por qué aparecen las alertas y cómo proceder
- **Guías de usuario**: Instrucciones paso a paso para manejar alertas de seguridad

### 🛡️ **ALERTA DE WINDOWS SMARTSCREEN**
- **Explicación educativa**: Documentación sobre por qué Windows marca ejecutables no firmados
- **Procedimiento seguro**: Pasos claros para ejecutar DotaTwin de manera segura
- **Alternativas**: Opciones para usuarios que prefieren ejecutar desde código fuente
- **Tranquilidad del usuario**: Garantías sobre la seguridad y transparencia del código

### 📋 **OPTIMIZACIONES TÉCNICAS**
- **Estructura de build mejorada**: Configuración optimizada para distribución
- **Ejecutable limpio**: Sin requerimientos de administrador ni accesos especiales
- **Metadatos del ejecutable**: Información detallada del archivo para reducir falsas alertas

### 🔧 **MEJORAS DE DOCUMENTACIÓN**
- **README expandido**: Sección completa sobre seguridad y procedimientos
- **Enlaces actualizados**: URLs correctas a GitHub Releases y comunidad Discord
- **Badges actualizados**: Versión v3.1.0 reflejada en toda la documentación

## [v3.0.0] - 2025-07-29 🎯 REBRANDING: DOTATWIN

### 🚀 **REBRANDING COMPLETO**
- **Nuevo nombre**: "Dota 2 Config Copier" → **"DotaTwin"**
- **Nueva identidad**: "Twin your Dota experience" - Crear gemelos perfectos de configuraciones
- **Versión mayor**: Incremento a v3.0.0 para reflejar el cambio significativo de marca
- **Concepto mejorado**: El nombre "Twin" refleja perfectamente la funcionalidad de duplicar/clonar configs

### 🔄 **CAMBIOS DE MARCA**
- **Aplicación**: Título actualizado a "DotaTwin v3.0.0"
- **Descripción**: "Twin your Dota experience - Copy configurations between Steam accounts"
- **Todos los archivos**: Actualizadas las referencias en código, documentación y configuración
- **Mantiene funcionalidad**: Sin cambios en características técnicas, solo rebranding

### � **MINOR FIXES**
- **GUI Paginación**: Corregido problema donde los controles de paginación no se mostraban visualmente
  - **Causa**: Inconsistencia en layout managers (mixing pack/grid) y falta de posicionamiento del frame
  - **Solución**: Consistencia en grid layout y agregado `frame.pack()` en PaginationWidget
  - **Resultado**: Controles de paginación ahora visibles cuando hay múltiples páginas

- **Icono de Barra de Tareas**: Implementado icono personalizado en barra de tareas de Windows
  - **Problema**: Al ejecutar como script Python, se mostraba icono de Python en lugar del icono de la app
  - **Solución**: Implementada API de Windows usando `ctypes` para forzar icono personalizado
  - **Mejoras técnicas**: 
    - App ID único de Windows (`Sadohu.DotaTwin.3.0.0`)
    - Uso de `LoadImageW()` y `SendMessageW()` para establecer iconos pequeño/grande
    - Configuración tardía con `root.after()` para máxima compatibilidad
  - **Resultado**: DotaTwin ahora muestra su icono `dota2.ico` en ventana, diálogos y barra de tareas

- **Ejecutable PyInstaller**: Corregido problema de icono en ejecutable empaquetado
  - **Problema**: El icono funcionaba en desarrollo pero no en el .exe generado
  - **Causa**: Rutas hardcodeadas que no funcionan cuando PyInstaller empaqueta la aplicación
  - **Solución**: Implementada detección automática de entorno con `sys.frozen` y `sys._MEIPASS`
  - **Mejoras técnicas**:
    - Nueva función `_get_resource_path()` para resolver rutas dinámicamente
    - Detección automática: desarrollo vs. ejecutable empaquetado
    - Uso de `sys._MEIPASS` para acceder a recursos en ejecutables
  - **Resultado**: Icono funciona perfectamente tanto en desarrollo como en ejecutable final

### 📁 **LIMPIEZA DE PROYECTO**
- **Estructura organizada**: Archivos temporales eliminados, assets organizados en `config/assets/`
- **Build config**: Archivos de PyInstaller movidos a `build_config/` 
- **Rutas actualizadas**: Spec files con rutas relativas correctas
- **Proyecto limpio**: Root del proyecto libre de archivos innecesarios

## [v3.0.0] - 2025-07-29 🎯 REBRANDING: DOTATWIN

### 🚀 **REBRANDING COMPLETO**
- **Nuevo nombre**: "Dota 2 Config Copier" → **"DotaTwin"**
- **Nueva identidad**: "Twin your Dota experience" - Crear gemelos perfectos de configuraciones
- **Versión mayor**: Incremento a v3.0.0 para reflejar el cambio significativo de marca
- **Concepto mejorado**: El nombre "Twin" refleja perfectamente la funcionalidad de duplicar/clonar configs

### 🔄 **CAMBIOS DE MARCA**
- **Aplicación**: Título actualizado a "DotaTwin v3.0.0"
- **Descripción**: "Twin your Dota experience - Copy configurations between Steam accounts"
- **Todos los archivos**: Actualizadas las referencias en código, documentación y configuración
- **Mantiene funcionalidad**: Sin cambios en características técnicas, solo rebranding

### � **MINOR FIXES**
- **GUI Paginación**: Corregido problema donde los controles de paginación no se mostraban visualmente
  - **Causa**: Inconsistencia en layout managers (mixing pack/grid) y falta de posicionamiento del frame
  - **Solución**: Consistencia en grid layout y agregado `frame.pack()` en PaginationWidget
  - **Resultado**: Controles de paginación ahora visibles cuando hay múltiples páginas

### �📁 **LIMPIEZA DE PROYECTO**
- **Estructura organizada**: Archivos temporales eliminados, assets organizados en `config/assets/`
- **Build config**: Archivos de PyInstaller movidos a `build_config/` 
- **Rutas actualizadas**: Spec files con rutas relativas correctas
- **Proyecto limpio**: Root del proyecto libre de archivos innecesarios

## [v2.1.2] - 2025-07-29 🔥 FIX CRÍTICO - Archivos .vcfg

### 🐛 **FIX CRÍTICO DE FUNCIONALIDAD**
- **🔥 Archivos .vcfg no se copiaban**: Problema crítico donde los archivos principales de Dota 2 no se estaban copiando
  - **Causa**: Método de copia selectiva con filtros demasiado restrictivos
  - **Impacto**: Solo se copiaban 2-3 archivos por cuenta en lugar de TODOS los archivos de configuración
  - **Solución**: Implementada copia completa de carpeta (como en v1) usando `shutil.copytree()`
  - **Método anterior**: Copia selectiva archivo por archivo con filtros
  - **Método actual**: Copia completa de toda la carpeta origen → destino
  - **Resultado**: Se copian TODOS los archivos de configuración sin excepciones

### � **CAMBIOS TÉCNICOS**
- **Simplificación del algoritmo de copia**: Revertido a método v1 comprobado y funcional
- **Eliminados filtros restrictivos**: Ya no se filtran archivos por extensión
- **Copia completa**: `shutil.copytree()` en lugar de copia selectiva
- **Mayor fiabilidad**: Garantiza que toda la configuración se copie correctamente

### ⚠️ **NOTA IMPORTANTE**
Este fix resuelve el problema principal reportado donde "la acción principal del sistema que es copiar la configuración no funciona correctamente". La aplicación ahora copia TODAS las configuraciones importantes de Dota 2, no solo archivos auxiliares.

## [v2.1.1] - 2025-07-29 🔧 CORRECCIONES CRÍTICAS DE GUI

### 🐛 **CORRECCIONES CRÍTICAS**
- **Problema de layout GUI**: Corregido problema donde elementos "origen-destino" y botones de acción no eran completamente visibles
- **Sistema de ignorar cuentas**: Corregido problema donde la función "ignorar" no actualizaba las listas en tiempo real
- **Sincronización de configuración**: Corregido desincronización entre instancias de configuración que causaba que los cambios no se reflejaran inmediatamente
- **🔥 CRÍTICO - Archivos .vcfg no se copiaban**: Agregado soporte para archivos `.vcfg` (Valve Configuration Files)
  - Los archivos principales de configuración de Dota 2 (user_convars, user_keys, machine_convars) no se estaban copiando
  - Incremento de archivos copiados de ~2 a ~8 por cuenta (400% más configuraciones)
  - Ahora incluye: keybinds, settings de usuario, configuraciones de máquina, etc.

### 🔧 **MEJORAS TÉCNICAS**
- **Layout responsivo con Grid**: Reemplazado sistema Pack por Grid layout para control preciso de posicionamiento
  - Widgets de estado y botones ahora siempre visibles en posiciones fijas
  - Notebook expansible pero respetando espacio reservado para controles
  - Configuración de peso para expansión controlada de elementos
- **Canvas con scroll**: Implementado sistema de scroll para listas de cuentas largas
  - Scroll vertical con rueda del mouse
  - Navegación fluida manteniendo elementos de control siempre visibles
- **Actualización forzada de interfaz**: Agregado `update_idletasks()` para forzar redibujado inmediato de widgets
- **Dimensiones de ventana optimizadas**: Altura mínima y por defecto aumentada a 800px para mejor visualización

### 🔄 **CORRECCIONES DE SINCRONIZACIÓN**
- **Referencia de configuración**: Agregada sincronización `self.app_config = self.config_service.config` después de ignorar/restaurar cuentas
- **Actualización en tiempo real**: Las listas de cuentas disponibles e ignoradas ahora se actualizan inmediatamente sin necesidad de reiniciar
- **Validación mejorada**: Agregada verificación de duplicados antes de ignorar cuentas con mensaje informativo

### 🖥️ **MEJORAS DE UX**
- **Diálogos modales mejorados**: Configuración `topmost` temporal para asegurar visibilidad de confirmaciones
- **Mensajes de éxito/error**: Agregados mensajes informativos después de ignorar/restaurar cuentas exitosamente
- **Validación de estados**: Verificación de cuentas ya ignoradas con mensaje informativo apropiado
- **AboutDialog interactivo**: Nuevo diálogo "Acerca de" con funcionalidades avanzadas
  - Texto seleccionable para copiar información
  - Enlaces clickeables (GitHub repository y Discord invite)
  - Botones específicos de copia: "💬 Copiar link de Discord" y "📋 Copiar link del Repositorio"
  - Información de contacto completa: Discord: Sadohu, GitHub: Sadohu
  - Enlace directo para unirse al Discord: https://discord.gg/MYNyKQvk
  - Copia directa de enlaces al portapapeles con confirmación visual

### 📊 **LOGGING DETALLADO**
- **Trazabilidad completa**: Logs detallados de todas las operaciones de ignorar/restaurar
- **Información de estado**: Logs con conteo preciso de cuentas disponibles/ignoradas después de cada operación
- **Seguimiento de sincronización**: Verificación en logs de actualización correcta de listas

### ✅ **VALIDACIÓN DE FUNCIONAMIENTO**
- ✅ Layout responsivo: Elementos siempre visibles independientemente del tamaño de ventana
- ✅ Scroll funcional: Navegación fluida en listas largas de cuentas
- ✅ Ignorar en tiempo real: Cuentas se mueven inmediatamente entre pestañas
- ✅ Restaurar en tiempo real: Cuentas restauradas aparecen inmediatamente en disponibles
- ✅ Persistencia correcta: Cambios se guardan correctamente en archivo JSON
- ✅ UX mejorada: Confirmaciones claras y mensajes informativos

### � **DISTRIBUCIÓN Y PACKAGING**
- **Ejecutable standalone v2.1.1**: Generado con PyInstaller
  - Archivo: `Dota2ConfigCopier_v2.1.1.exe` (~14.6 MB)
  - Sin dependencias externas (Python embebido)
  - Compresión UPX para tamaño optimizado
  - Icono y recursos integrados
  - Compatible con Windows 10/11 (64-bit)
- **README de distribución**: Documentación completa para usuarios finales
- **Configuración de build**: Spec file optimizado con exclusiones y optimizaciones

### �📁 **REORGANIZACIÓN DE ESTRUCTURA**
- **Directorio raíz limpio**: Movidos archivos de documentación duplicados y scripts auxiliares
- **Scripts organizados**: Todos los scripts de testing/verificación movidos a `tests/scripts/`
- **Documentación centralizada**: Archivos técnicos consolidados en `docs/`
- **Estructura profesional**: Directorio raíz solo con archivos esenciales para mejor navegación

### 📋 **ARCHIVOS REORGANIZADOS**
- `test_*.py` y `verificar_*.py` → `tests/scripts/`
- Documentación técnica mantenida en `docs/`
- `README.md` creado para `tests/scripts/` con documentación de scripts auxiliares
- `REORGANIZACION_v2.1.1.md` documenta todos los cambios estructurales

---

## [v2.1.0] - 2025-07-29 🔧 CONFIGURACIÓN AVANZADA DE STEAM

### ✨ **NUEVAS FUNCIONALIDADES**
- **Detección automática mejorada de Steam**: Busca en múltiples ubicaciones estándar
- **Configuración manual de Steam**: Permite seleccionar ubicación personalizada cuando no se detecta automáticamente
- **Menú de configuración**: Nueva barra de menú con opciones avanzadas
- **Persistencia de configuración**: Las rutas personalizadas se guardan automáticamente
- **Soporte para Steam Microsoft Store**: Detecta instalaciones desde Microsoft Store

### 🔧 **MEJORAS DE CONFIGURACIÓN**
- **Prompt automático**: Si Steam no se detecta, solicita ubicación al usuario
- **Validación robusta**: Verifica que la ubicación contiene una instalación válida de Steam
- **Múltiples rutas**: Soporte para Steam en ubicaciones no estándar
- **Reconfiguración en tiempo real**: Cambiar ubicación de Steam sin reiniciar la aplicación

### 🖥️ **INTERFAZ MEJORADA**
- **Menú Archivo**: Recargar cuentas, salir
- **Menú Configuración**: Configurar Steam, detección automática
- **Menú Ayuda**: Información sobre la aplicación
- **Diálogos informativos**: Mensajes claros sobre el estado de Steam

### 🧪 **TESTING EXPANDIDO**
- **10 nuevos tests**: Validación completa de configuración de Steam
- **Tests de integración**: Flujo completo de detección y configuración
- **Cobertura mejorada**: Validación de rutas, configuración personalizada, persistencia

### 🏗️ **ARQUITECTURA EXTENDIDA**
- **SteamConfigurationService**: Nuevo servicio para gestión de configuración de Steam
- **SteamConfigDialog**: Diálogo modular para configuración avanzada
- **Validación de rutas**: Métodos robustos para verificar instalaciones de Steam
- **Configuración persistente**: AppConfig extendido con custom_steam_path

### 🔄 **COMPATIBILIDAD PRESERVADA**
- **Detección automática**: Funciona igual que v2.0 cuando Steam está en ubicación estándar
- **Configuración existente**: Las configuraciones anteriores se mantienen
- **Funcionalidad core**: Toda la funcionalidad de copia de configuraciones preservada

### 📋 **CASOS DE USO SOPORTADOS**
- ✅ Steam en `C:\\Program Files (x86)\\Steam` (estándar)
- ✅ Steam en `C:\\Program Files\\Steam`
- ✅ Steam en unidades alternativas (D:, E:, F:)
- ✅ Steam desde Microsoft Store
- ✅ Instalaciones portables de Steam
- ✅ Configuración manual para cualquier ubicación

---

## [v2.0.0] - 2025-07-29 🚀 REFACTORIZACIÓN COMPLETA - ARQUITECTURA MODULAR

### ✨ **NUEVA ARQUITECTURA MODULAR**
- **Separación de responsabilidades**: Código organizado en módulos especializados
- **Principios SOLID**: Aplicación completa de mejores prácticas de desarrollo
- **Arquitectura en capas**: Domain, Application, Infrastructure separadas
- **Servicios de negocio**: Lógica encapsulada en servicios dedicados
- **Componentes UI reutilizables**: Widgets modulares y consistentes

### 🏗️ **ESTRUCTURA MODULAR**
- **`src/models/`**: Modelos de dominio (SteamAccount, PaginationInfo, AppConfig)
- **`src/core/`**: Servicios de negocio (SteamAccountService, ConfigurationService)
- **`src/gui/`**: Componentes de interfaz (AccountListWidget, PaginationWidget)
- **`src/utils/`**: Utilidades comunes (LoggingMixin, AvatarManager)
- **`config/`**: Configuración centralizada y constantes
- **`tests/`**: Suite completa de tests automatizados

### 🔧 **SERVICIOS ESPECIALIZADOS**
- **SteamAccountService**: Detección y gestión de cuentas Steam
- **AccountFilterService**: Filtrado y organización de cuentas
- **ConfigurationService**: Gestión de configuración persistente
- **FileCopyService**: Operaciones de copia con backup automático
- **ValidationService**: Validaciones de negocio centralizadas

### 🖥️ **COMPONENTES UI MODULARES**
- **Dota2ConfigCopierApp**: Aplicación principal coordinadora (MVC)
- **AccountListWidget**: Lista de cuentas con paginación integrada
- **PaginationWidget**: Controles de paginación reutilizables
- **StatusWidget**: Estado de selección con validación visual
- **ActionButtonsWidget**: Botones de acción con habilitación condicional

### 🧪 **TESTING AUTOMATIZADO**
- **Tests unitarios**: Validación de modelos de dominio
- **Tests de servicios**: Verificación de lógica de negocio
- **Tests de paginación**: Validación de cálculos y navegación
- **Ejecución**: `python -m tests.test_refactor`

### 📊 **SISTEMA DE LOGGING**
- **LoggingMixin**: Logging automático por clase
- **PerformanceLogger**: Medición de tiempo de operaciones
- **OperationContext**: Context manager para operaciones complejas
- **Niveles configurables**: DEBUG, INFO, WARNING, ERROR

### 🔄 **COMPATIBILIDAD TOTAL**
- **Migración automática**: Configuraciones v1.3 se migran sin intervención
- **Funcionalidad preservada**: Todas las características de v1.3 disponibles
- **Coexistencia**: v1.3 (`dota_main_config.py`) y v2.0 (`main.py`) pueden usarse
- **Datos conservados**: Cuentas ignoradas, selecciones y preferencias se mantienen

### 📚 **DOCUMENTACIÓN TÉCNICA**
- **ARQUITECTURA_MODULAR.md**: Documentación completa de la nueva arquitectura
- **MIGRACION_V2.md**: Guía detallada de migración para desarrolladores
- **requirements.txt**: Gestión de dependencias centralizada
- **main.py**: Punto de entrada principal con validaciones

### 🚀 **MEJORAS DE RENDIMIENTO**
- **Carga lazy**: Avatares y recursos se cargan bajo demanda
- **Caché inteligente**: Gestión eficiente de memoria
- **Navegación optimizada**: Renderizado eficiente de páginas
- **Limpieza automática**: Gestión de recursos y backups

### 🔧 **EXTENSIBILIDAD**
- **Sistema de plugins preparado**: Base para funcionalidades modulares
- **Interfaces bien definidas**: Fácil agregar nuevos servicios
- **Componentes reutilizables**: Widgets aplicables a otros contextos
- **Configuración flexible**: Settings centralizados y expandibles

---

## [v1.3] - 2025-07-29

### ✨ Agregado
- **Iconos en botones**: Implementación de iconos Unicode para mejor UX
  - 📤 Origen: Botón para seleccionar cuenta fuente
  - 📥 Destino: Botón para seleccionar cuenta receptora
  - 🚫 Ignorar: Botón para ocultar cuentas del listado
  - ↩️ Restaurar: Botón para devolver cuentas ignoradas
  - ❌ Cancelar selección: Botón para limpiar selecciones
  - 📋 Copiar configuración: Botón para ejecutar la copia
  - ⬅️ ➡️ Navegación: Botones de páginas anterior/siguiente
  - 🎮 🔕 📄 Títulos: Iconos descriptivos en títulos de sección

### 🔧 Mejorado
- **Interfaz visual**: Mayor claridad y profesionalismo con iconos descriptivos
- **Accesibilidad**: Reconocimiento rápido de funciones sin leer texto
- **Consistencia**: Uso coherente de iconos relacionados en toda la aplicación

---

## [v1.2] - 2025-07-29

### ✨ Agregado
- **Sistema de paginación completo**: Gestión eficiente de listas grandes de cuentas
  - Control personalizable de elementos por página (10, 15, 20, 25, 30)
  - Navegación con botones numerados (muestra hasta 5 páginas)
  - Botones "Anterior" y "Siguiente" para navegación secuencial
  - Información de página actual y total de elementos
- **Auto-navegación inteligente**: 
  - Navega automáticamente a páginas que contienen origen/destino seleccionados
  - Prioridad de navegación: origen > destino
  - Preservación de selecciones entre cambios de página
- **Persistencia de configuración de paginación**: Guarda preferencia de elementos por página

### 🔧 Mejorado
- **Rendimiento**: Mejor manejo de memoria con listas grandes de cuentas
- **Experiencia de usuario**: Navegación fluida sin scroll infinito
- **Lógica de navegación**: Evita sobreescribir navegación manual del usuario

### 🐛 Corregido
- **Bug de paginación**: Navegación manual ahora funciona correctamente
- **Interferencia de auto-navegación**: Separación clara entre navegación automática y manual
- **Límites de página**: Validación correcta de páginas válidas

### 📄 Documentación
- Creación de `PAGINACION_IMPLEMENTADA.md` con detalles técnicos

---

## [v1.1] - 2025-07-29

### ✨ Agregado
- **Sistema de cuentas ignoradas**: 
  - Botón "Ignorar" para ocultar cuentas del listado principal
  - Pestaña "Cuentas Ignoradas" para gestionar cuentas ocultas
  - Botón "Restaurar" para devolver cuentas al listado principal
- **Interfaz con pestañas**:
  - Pestaña "Cuentas Disponibles" (listado principal)
  - Pestaña "Cuentas Ignoradas" (gestión de cuentas ocultas)
- **Gestión expandida de configuración JSON**:
  - Campo `cuentas_ignoradas` para persistir lista de cuentas ocultas
  - Migración automática desde formato de configuración v1.0
  - Funciones robustas de carga/guardado con validación de errores

### 🔧 Mejorado
- **Organización de interfaz**: Pestañas para mejor organización visual
- **Flexibilidad**: Fácil gestión de cuentas frecuentes vs. poco usadas
- **Persistencia**: Todas las preferencias se mantienen entre sesiones
- **Compatibilidad**: Migración automática desde configuraciones antiguas

### 🐛 Corregido
- **KeyError en cuentas_ignoradas**: Manejo robusto de archivos JSON existentes
- **Validación de estructura JSON**: Verificación y corrección automática de campos faltantes

### 📄 Documentación
- Creación de `CAMBIOS_IMPLEMENTADOS.md` con detalles de implementación
- Script `migrar_json.py` para migración de configuraciones

---

## [v1.0] - 2025-07-29 (Versión Base)

### ✨ Características Iniciales
- **Detección automática de cuentas Steam**: Escaneo de userdata para cuentas con Dota 2
- **Extracción de información de usuario**:
  - Nombres de usuario desde localconfig.vdf
  - Avatares desde caché de Steam
  - SteamID y rutas de configuración
- **Interfaz gráfica básica**:
  - Lista de cuentas detectadas
  - Botones "Origen" y "Destino" para selección
  - Botón "Copiar configuración" para ejecutar transferencia
  - Botón "Cancelar selección" para limpiar selecciones
- **Sistema de selección visual**:
  - Colores distintivos para origen (azul) y destino (verde)
  - Estados deshabilitados para prevenir selecciones inválidas
- **Copia completa de configuración**: Transferencia de todos los archivos de Dota 2
- **Persistencia básica**: Guardado de última selección origen/destino
- **Validación de seguridad**: Confirmaciones antes de sobrescribir configuraciones
- **Manejo de errores**: Tratamiento adecuado de errores de E/O y permisos

### 🏗️ Arquitectura Base
- **Estructura modular**: Separación clara entre lógica y interfaz
- **Gestión de archivos**: Funciones robustas para copia recursiva
- **Configuración JSON**: Sistema simple de persistencia
- **Interfaz tkinter**: GUI nativa multiplataforma

---

## 🔄 Patrones de Versionado

### Incremento de Versiones
- **Major (X.0)**: Cambios incompatibles o reestructuración completa
- **Minor (X.Y)**: Nuevas funcionalidades manteniendo compatibilidad
- **Patch (X.Y.Z)**: Correcciones de bugs y mejoras menores

### Categorías de Cambios
- **✨ Agregado**: Nuevas funcionalidades
- **🔧 Mejorado**: Mejoras en funcionalidades existentes
- **🐛 Corregido**: Corrección de bugs
- **📄 Documentación**: Cambios en documentación
- **🔒 Seguridad**: Correcciones de vulnerabilidades
- **⚠️ Deprecado**: Funcionalidades que serán removidas
- **🗑️ Removido**: Funcionalidades eliminadas

---

## 🎯 Próximas Versiones

### v1.4 (Planificado)
- [ ] Sistema de backup automático antes de copiar
- [ ] Configuraciones específicas (hotkeys, video, audio por separado)
- [ ] Modo portable sin instalación
- [ ] Validación de integridad de archivos

### v1.5 (Futuro)
- [ ] Soporte para otros juegos de Steam
- [ ] Interfaz web opcional
- [ ] Sincronización automática entre cuentas
- [ ] Perfiles de configuración preestablecidos

---

*Para más detalles sobre implementaciones específicas, consultar archivos de documentación en la carpeta `docs/`*
