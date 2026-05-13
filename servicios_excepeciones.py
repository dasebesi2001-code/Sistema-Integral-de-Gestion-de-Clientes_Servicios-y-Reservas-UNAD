"""
servicios_excepeciones.py
Excepciones personalizadas y logger del Sistema Software FJ
Universidad Nacional Abierta y a Distancia - UNAD
Curso: Programación 213023
"""

#Propuesta de cambio de codigo - Jesus Solis
"""import logging
class ProyectoError(Exception):
    #clase base para las excepciones en este módulo.
    pass    


class elemento_no_encontrado(ProyectoError):
    #se lanza cuando no se encuentra un elemento específico en la base de datos o en la colección.
    pass

class ValidacionError(ProyectoError):
    #se lanza cuando se produce un error de validación en los datos de entrada.
    pass
    """
import logging
 
# ---------------------------------------------------------------------------
# Configuración del logger (registro en archivo)
# ---------------------------------------------------------------------------
logging.basicConfig(
    filename='errores_sistemas.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
 
# ---------------------------------------------------------------------------
# JERARQUÍA DE EXCEPCIONES PERSONALIZADAS
# ---------------------------------------------------------------------------
 
class ProyectoError(Exception):
    """Clase base para todas las excepciones del sistema Software FJ."""
    pass
 
 
class elemento_no_encontrado(ProyectoError):
    """Se lanza cuando no se encuentra un elemento en la colección."""
    pass
 
 
class ValidacionError(ProyectoError):
    """Se lanza cuando se produce un error de validación en los datos de entrada."""
    pass
 
 
class ClienteInvalidoError(ValidacionError):
    """Se lanza cuando los datos del cliente no son válidos."""
    pass
 
 
class ServicioInvalidoError(ValidacionError):
    """Se lanza cuando los parámetros de un servicio no son válidos."""
    pass
 
 
class ServicioNoDisponibleError(ProyectoError):
    """Se lanza cuando el servicio solicitado no está disponible."""
    def __init__(self, nombre_servicio: str):
        super().__init__(f"El servicio '{nombre_servicio}' no está disponible.")
 
 
class ReservaInvalidaError(ProyectoError):
    """Se lanza cuando una reserva tiene datos o estado inválidos."""
    pass
 
 
class DuracionInvalidaError(ReservaInvalidaError):
    """Se lanza cuando la duración está fuera del rango permitido."""
    def __init__(self, duracion, minimo, maximo):
        super().__init__(
            f"Duración '{duracion}' inválida. Debe estar entre {minimo} y {maximo}."
        )
 
 
class OperacionNoPermitidaError(ProyectoError):
    """Se lanza cuando se intenta una operación no permitida sobre una reserva."""
    pass
 
 
class CalculoCostoError(ProyectoError):
    """Se lanza cuando ocurre un error durante el cálculo de costos."""
    pass