# 🧪 Scripts de Testing y Verificación

Esta carpeta contiene scripts auxiliares para testing manual, verificación del proyecto y validación de la interfaz.

## 📄 **Archivos Incluidos**

### **Scripts de Testing Manual**
- **`test_dialog.py`**: Script específico para probar diálogos de confirmación
- **`test_ignore.py`**: Script para probar la funcionalidad de ignorar cuentas
- **`test_visual.py`**: Script para verificar elementos visuales de la interfaz

### **Scripts de Verificación del Proyecto**
- **`verificar_proyecto.py`**: Validación completa del estado del proyecto v2.0
  - Verificación de módulos e importaciones
  - Validación de servicios principales
  - Comprobación de componentes UI
  - Ejecución de tests automatizados
  - Verificación de configuración

### **Scripts de Verificación de Layout**
- **`verificar_layout.py`**: Verificación básica del layout de la interfaz
- **`verificacion_layout_final.py`**: Validación final del layout después de correcciones

## 🔧 **Uso**

### Ejecutar scripts individuales:
```bash
# Desde el directorio raíz del proyecto
python tests/scripts/verificar_proyecto.py
python tests/scripts/test_dialog.py
python tests/scripts/test_ignore.py
```

### Scripts de verificación de layout:
```bash
python tests/scripts/verificar_layout.py
python tests/scripts/verificacion_layout_final.py
```

## 📋 **Propósito**

Estos scripts fueron creados durante el desarrollo y debugging de v2.1.x para:

1. **Validar funcionalidad específica** sin ejecutar toda la aplicación
2. **Verificar correcciones de layout** antes del deployment
3. **Testing manual dirigido** de componentes específicos
4. **Diagnóstico rápido** de problemas durante desarrollo

## ⚠️ **Nota**

Estos son scripts auxiliares de desarrollo. Para testing automatizado completo, usar:
```bash
python -m tests.test_refactor
python -m tests.test_steam_config
```
