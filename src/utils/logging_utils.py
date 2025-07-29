"""
Utilidades de logging para la aplicación Dota 2 Config Copier.

Este módulo configura el sistema de logging de manera centralizada
siguiendo las mejores prácticas para debugging y monitoreo.
"""

import logging
import logging.config
from pathlib import Path
from typing import Optional
from config.settings import LOGGING_CONFIG, PROJECT_ROOT


def setup_logging(log_level: str = "INFO", 
                 log_file: Optional[Path] = None) -> None:
    """
    Configura el sistema de logging de la aplicación.
    
    Args:
        log_level: Nivel de logging ("DEBUG", "INFO", "WARNING", "ERROR")
        log_file: Archivo de log personalizado (opcional)
    """
    # Usar configuración de settings si no se especifica archivo
    config = LOGGING_CONFIG.copy()
    
    if log_file:
        config["handlers"]["file"]["filename"] = str(log_file)
    
    # Asegurar que el directorio de logs existe
    log_path = Path(config["handlers"]["file"]["filename"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configurar nivel de logging
    config["handlers"]["console"]["level"] = log_level
    config["loggers"][""]["level"] = log_level
    
    # Aplicar configuración
    logging.config.dictConfig(config)
    
    # Log inicial
    logger = logging.getLogger(__name__)
    logger.info(f"Sistema de logging configurado - Nivel: {log_level}")


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para un módulo específico.
    
    Args:
        name: Nombre del módulo (__name__ generalmente)
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


class LoggingMixin:
    """
    Mixin para agregar capacidades de logging a cualquier clase.
    
    Proporciona un logger automático basado en el nombre de la clase.
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Obtiene el logger para esta clase."""
        return logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
    
    def log_method_call(self, method_name: str, **kwargs) -> None:
        """
        Registra la llamada a un método con sus parámetros.
        
        Args:
            method_name: Nombre del método
            **kwargs: Parámetros del método
        """
        params = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        self.logger.debug(f"{method_name}({params})")
    
    def log_error(self, error: Exception, context: str = "") -> None:
        """
        Registra un error con contexto adicional.
        
        Args:
            error: Excepción ocurrida
            context: Contexto adicional del error
        """
        context_msg = f" - {context}" if context else ""
        self.logger.error(f"Error: {error}{context_msg}", exc_info=True)


class PerformanceLogger:
    """
    Logger especializado para medir rendimiento de operaciones.
    
    Permite medir tiempo de ejecución y recursos utilizados.
    """
    
    def __init__(self, logger_name: str = "performance"):
        self.logger = logging.getLogger(logger_name)
        self._start_times = {}
    
    def start_operation(self, operation_name: str) -> None:
        """
        Inicia el tracking de una operación.
        
        Args:
            operation_name: Nombre de la operación
        """
        import time
        self._start_times[operation_name] = time.time()
        self.logger.debug(f"Iniciando operación: {operation_name}")
    
    def end_operation(self, operation_name: str) -> float:
        """
        Termina el tracking de una operación y registra el tiempo.
        
        Args:
            operation_name: Nombre de la operación
            
        Returns:
            Tiempo transcurrido en segundos
        """
        import time
        
        if operation_name not in self._start_times:
            self.logger.warning(f"Operación no iniciada: {operation_name}")
            return 0.0
        
        elapsed = time.time() - self._start_times[operation_name]
        del self._start_times[operation_name]
        
        self.logger.info(f"Operación '{operation_name}' completada en {elapsed:.3f}s")
        return elapsed
    
    def log_memory_usage(self, context: str = "") -> None:
        """
        Registra el uso actual de memoria.
        
        Args:
            context: Contexto para el log
        """
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            context_msg = f" - {context}" if context else ""
            self.logger.debug(f"Uso de memoria: {memory_mb:.1f}MB{context_msg}")
            
        except ImportError:
            self.logger.debug("psutil no disponible para medir memoria")


def log_function_calls(func):
    """
    Decorador para loggear automáticamente llamadas a funciones.
    
    Args:
        func: Función a decorar
        
    Returns:
        Función decorada
    """
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        
        # Log entrada
        args_str = ", ".join(str(arg) for arg in args)
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        params = ", ".join(filter(None, [args_str, kwargs_str]))
        
        logger.debug(f"Llamando {func.__name__}({params})")
        
        try:
            # Ejecutar función
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {e}", exc_info=True)
            raise
    
    return wrapper


def create_file_handler(log_file: Path, 
                       level: str = "DEBUG",
                       format_string: Optional[str] = None) -> logging.FileHandler:
    """
    Crea un handler de archivo personalizado.
    
    Args:
        log_file: Archivo de destino
        level: Nivel de logging
        format_string: Formato personalizado (opcional)
        
    Returns:
        Handler configurado
    """
    # Asegurar que el directorio existe
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setLevel(getattr(logging, level.upper()))
    
    # Formato por defecto si no se especifica
    if not format_string:
        format_string = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
    
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    
    return handler


def setup_debug_logging(debug_file: Optional[Path] = None) -> None:
    """
    Configura logging detallado para debugging.
    
    Args:
        debug_file: Archivo específico para debug (opcional)
    """
    if not debug_file:
        debug_file = PROJECT_ROOT / "debug.log"
    
    # Crear handler de debug
    debug_handler = create_file_handler(
        debug_file, 
        level="DEBUG",
        format_string="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(funcName)s() - %(message)s"
    )
    
    # Agregar a todos los loggers
    root_logger = logging.getLogger()
    root_logger.addHandler(debug_handler)
    root_logger.setLevel(logging.DEBUG)
    
    logging.info(f"Logging de debug habilitado: {debug_file}")


class OperationContext:
    """
    Context manager para loggear operaciones complejas.
    
    Automáticamente registra inicio, fin y manejo de errores.
    """
    
    def __init__(self, operation_name: str, logger: Optional[logging.Logger] = None):
        self.operation_name = operation_name
        self.logger = logger or logging.getLogger(__name__)
        self.performance_logger = PerformanceLogger()
    
    def __enter__(self):
        self.logger.info(f"Iniciando: {self.operation_name}")
        self.performance_logger.start_operation(self.operation_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = self.performance_logger.end_operation(self.operation_name)
        
        if exc_type is None:
            self.logger.info(f"Completado: {self.operation_name} ({elapsed:.3f}s)")
        else:
            self.logger.error(f"Error en: {self.operation_name} - {exc_val}", exc_info=True)
        
        return False  # No suprimir excepciones
