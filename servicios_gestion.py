import logging
import json
import os 
from servicio_modelos import servicio
from servicios_excepeciones import ValidacionError, ProyectoError

logging.basicConfig(
    filename='errores_sistemas.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
class cliente:
    def __init__(self, id, nombre, correo):
        self.__id = id
        self._nombre = nombre
        self._correo = correo
        
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        raise ValidacionError("El ID no se puede modificar después de la creación del cliente.")

class reservas:
    def __init__(self, id_reservas, cliente, servicio, fecha_reserva):
        self.__id_reservas = id_reservas
        self.cliente = cliente
        self.servicio = servicio
        self._fecha_reserva = fecha_reserva
        self.estado = "confirmada"
    
    def procesar_confirmacion(self):
        
        costo_total = self.servicio.calcular_costo_total()
        return costo_total

class registro_reservas:
    def __init__(self):
        self.reservas = []
    
    def agregar_reserva(self, id_reserva, cliente, servicio, fecha_reserva):
        try:
            if not isinstance(servicio, servicio):
                raise ValidacionError("El servicio proporcionado no es válido.")
            nueva = reservas(id_reserva, cliente, servicio, fecha_reserva)
            costo_nueva = nueva.procesar_confirmacion()
            self.reservas.append(nueva)
            return costo_nueva
        except ProyectoError as e:
            logging.error(f"Error al agregar reserva: id_reserva={id_reserva}:{e}")
            return f"Error controlado: {e}"
        except Exception as e:
            logging.error(f"error inesperado al agregar reserva: id_reserva={id_reserva}:{e}")
            return "Error inesperado al agregar reserva. Por favor, inténtelo de nuevo más tarde."