# 📝 CHANGELOG

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

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
