# 🏗️ Arquitectura Modular v2.0 - Dota 2 Config Copier

## 📋 Descripción General

Este documento describe la nueva arquitectura modular implementada en la versión 2.0 de Dota 2 Config Copier. La refactorización sigue principios de diseño de software moderno para mejorar la mantenibilidad, testabilidad y extensibilidad del código.

## 🎯 Principios de Diseño Aplicados

### 1. **SOLID Principles**
- **Single Responsibility**: Cada clase tiene una responsabilidad específica
- **Open/Closed**: Extensible sin modificar código existente
- **Liskov Substitution**: Interfaces bien definidas y sustituibles
- **Interface Segregation**: Interfaces específicas y cohesivas
- **Dependency Inversion**: Dependencias hacia abstracciones

### 2. **Clean Architecture**
- Separación clara entre capas de dominio, aplicación e infraestructura
- Independencia de frameworks externos
- Testabilidad sin dependencias externas

### 3. **Domain-Driven Design (DDD)**
- Modelos de dominio ricos
- Servicios de dominio específicos
- Separación clara de contextos

## 📁 Estructura del Proyecto

```
dota2-config-copier/
├── src/                           # Código fuente principal
│   ├── models/                    # Modelos de dominio
│   │   ├── __init__.py
│   │   └── domain_models.py       # Entidades y objetos de valor
│   ├── core/                      # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── steam_service.py       # Servicios de Steam
│   │   └── config_service.py      # Servicios de configuración
│   ├── gui/                       # Interfaz de usuario
│   │   ├── __init__.py
│   │   ├── main_app.py           # Aplicación principal
│   │   ├── main_tab.py           # Componentes pestaña principal
│   │   └── ignored_tab.py        # Componentes pestaña ignoradas
│   └── utils/                     # Utilidades comunes
│       ├── __init__.py
│       ├── logging_utils.py       # Sistema de logging
│       └── ui_utils.py            # Utilidades de interfaz
├── config/                        # Configuración centralizada
│   ├── __init__.py
│   └── settings.py               # Constantes y configuraciones
├── tests/                         # Tests unitarios
│   └── test_refactor.py          # Tests de validación
├── docs/                          # Documentación existente
├── main.py                        # Punto de entrada principal
└── README.md                      # Documentación actualizada
```

## 🔧 Componentes Principales

### 1. **Modelos de Dominio** (`src/models/`)

#### `SteamAccount`
- Representa una cuenta de Steam con Dota 2
- Encapsula lógica de conversión de IDs y validaciones
- Inmutable y con métodos de consulta

#### `PaginationInfo`
- Maneja toda la lógica de paginación
- Cálculos de páginas, navegación y rangos
- Reutilizable en diferentes contextos

#### `AppSelection`
- Representa la selección actual de origen/destino
- Validaciones de negocio integradas
- Estados bien definidos

#### `AppConfig`
- Configuración persistente de la aplicación
- Migración automática de versiones
- Carga y guardado seguro

### 2. **Servicios de Negocio** (`src/core/`)

#### `SteamAccountService`
- **Responsabilidad**: Detección y gestión de cuentas Steam
- **Métodos principales**:
  - `find_accounts_with_dota2()`: Detecta cuentas con Dota 2
  - `refresh_account_info()`: Actualiza información de cuenta
  - `validate_account()`: Valida configuración de cuenta

#### `AccountFilterService`
- **Responsabilidad**: Filtrado y organización de cuentas
- **Métodos principales**:
  - `filter_available_accounts()`: Filtra cuentas no ignoradas
  - `filter_ignored_accounts()`: Filtra cuentas ignoradas
  - `find_account_by_id()`: Búsqueda por ID
  - `sort_accounts()`: Ordenamiento por criterios

#### `ConfigurationService`
- **Responsabilidad**: Gestión de configuración persistente
- **Métodos principales**:
  - `load_config()`: Carga configuración
  - `save_config()`: Guarda configuración
  - `ignore_account()`: Maneja cuentas ignoradas
  - `update_pagination_settings()`: Actualiza paginación

#### `FileCopyService`
- **Responsabilidad**: Operaciones de copia de archivos
- **Métodos principales**:
  - `copy_configuration()`: Copia configuración
  - `validate_paths()`: Valida rutas de copia
  - `cleanup_old_backups()`: Mantenimiento de backups

### 3. **Interfaz de Usuario** (`src/gui/`)

#### `Dota2ConfigCopierApp`
- **Responsabilidad**: Coordinación general de la aplicación
- **Patrón**: Controller principal (MVC)
- **Funciones**:
  - Inicialización de servicios
  - Coordinación entre componentes
  - Manejo de eventos principales

#### `AccountListWidget`
- **Responsabilidad**: Lista de cuentas con paginación
- **Características**:
  - Renderizado eficiente
  - Paginación integrada
  - Gestión de selección

#### `PaginationWidget`
- **Responsabilidad**: Controles de paginación reutilizables
- **Características**:
  - Auto-renderizado
  - Navegación por botones
  - Información de estado

#### `StatusWidget` y `ActionButtonsWidget`
- **Responsabilidad**: Estado y acciones de la aplicación
- **Características**:
  - Validación visual
  - Habilitación condicional
  - Feedback al usuario

### 4. **Utilidades** (`src/utils/`)

#### `LoggingMixin`
- **Responsabilidad**: Sistema de logging integrado
- **Características**:
  - Logging automático por clase
  - Performance tracking
  - Context managers

#### `AvatarManager`
- **Responsabilidad**: Gestión de avatares con caché
- **Características**:
  - Caché automático
  - Carga lazy
  - Limpieza de recursos

#### `MessageHelper`
- **Responsabilidad**: Diálogos consistentes
- **Características**:
  - Iconos integrados
  - Mensajes estandarizados
  - Confirmaciones consistentes

## 🔄 Flujo de Datos

### 1. **Inicialización**
```
main.py → Dota2ConfigCopierApp → Services → UI Components
```

### 2. **Detección de Cuentas**
```
SteamAccountService → AccountFilterService → UI Update
```

### 3. **Selección de Cuenta**
```
UI Event → AppSelection → ConfigurationService → UI Update
```

### 4. **Copia de Configuración**
```
UI Event → ValidationService → FileCopyService → Feedback
```

## 📊 Beneficios de la Arquitectura

### 1. **Mantenibilidad**
- **Separación de responsabilidades**: Cada módulo tiene un propósito específico
- **Bajo acoplamiento**: Cambios en un módulo no afectan otros
- **Alta cohesión**: Funcionalidad relacionada agrupada

### 2. **Testabilidad**
- **Inyección de dependencias**: Fácil mockeo para tests
- **Servicios aislados**: Tests unitarios independientes
- **Validación automática**: Tests de regresión

### 3. **Extensibilidad**
- **Nuevos servicios**: Fácil agregar funcionalidad
- **Nuevos widgets**: Composición de UI modular
- **Nuevas configuraciones**: Sistema flexible

### 4. **Reutilización**
- **Componentes modulares**: Widgets reutilizables
- **Servicios genéricos**: Lógica aplicable a otros contextos
- **Utilidades compartidas**: Helpers comunes

## 🔧 Patrones de Diseño Implementados

### 1. **Model-View-Controller (MVC)**
- **Model**: `domain_models.py` y servicios
- **View**: Componentes UI en `gui/`
- **Controller**: `Dota2ConfigCopierApp`

### 2. **Service Layer**
- Servicios de negocio en `core/`
- Abstracción de lógica compleja
- Reutilización entre componentes

### 3. **Repository Pattern**
- `ConfigurationService` como repositorio de configuración
- Abstracción de persistencia
- Migración automática de datos

### 4. **Factory Pattern**
- `WidgetFactory` para creación de widgets
- Configuración consistente
- Reducción de código repetitivo

### 5. **Observer Pattern**
- Callbacks entre componentes UI
- Eventos de selección y cambios
- Actualización reactiva

## 🧪 Testing Strategy

### 1. **Tests Unitarios**
- Cada servicio con tests independientes
- Modelos de dominio validados
- Utilidades con cobertura completa

### 2. **Tests de Integración**
- Flujos completos de usuario
- Interacción entre servicios
- Persistencia de configuración

### 3. **Tests de UI**
- Componentes renderizados correctamente
- Eventos manejados apropiadamente
- Estados visuales consistentes

## 🚀 Roadmap de Mejoras

### v2.1 - Próximas Mejoras
- [ ] Sistema de plugins
- [ ] API REST opcional
- [ ] Configuración por archivo YAML
- [ ] Tests automatizados completos

### v2.2 - Funcionalidades Avanzadas
- [ ] Sincronización automática
- [ ] Perfiles de configuración
- [ ] Backup inteligente
- [ ] Soporte multi-juego

### v3.0 - Arquitectura Distribuida
- [ ] Microservicios opcionales
- [ ] Base de datos externa
- [ ] Cliente web
- [ ] API pública

## 📝 Guía de Contribución

### 1. **Agregar Nueva Funcionalidad**
1. Crear modelo de dominio si es necesario
2. Implementar servicio de negocio
3. Crear componente UI correspondiente
4. Agregar tests unitarios
5. Actualizar documentación

### 2. **Modificar Funcionalidad Existente**
1. Identificar componente afectado
2. Verificar impacto en otros módulos
3. Ejecutar tests de regresión
4. Actualizar tests si es necesario

### 3. **Convenciones de Código**
- Seguir PEP 8 para Python
- Documentar métodos públicos
- Usar type hints
- Nombres descriptivos en inglés

## 🔍 Migración desde v1.3

### 1. **Compatibilidad**
- Configuración automáticamente migrada
- Misma funcionalidad disponible
- Interfaz familiar para usuarios

### 2. **Mejoras Visibles**
- Mejor rendimiento
- Logging detallado
- Manejo de errores robusto
- Extensibilidad futura

### 3. **Cambios Internos**
- Estructura de código completamente refactorizada
- Separación clara de responsabilidades
- Base sólida para futuras mejoras

---

*Esta arquitectura establece las bases para un crecimiento sostenible del proyecto, manteniendo la simplicidad para el usuario final mientras proporciona flexibilidad para los desarrolladores.*
