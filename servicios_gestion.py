
import json
import os 
import servicio_modelos
class cliente:
    def __init__(self, id, nombre, correo):
        self._id = id
        self._nombre = nombre
        self._correo = correo
        
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        raise AttributeError("El ID no se puede modificar después de la creación del cliente.")
    
class reservas(cliente):
    def __init__(self, id, nombre, correo):
        super().__init__(id, nombre, correo)
        self.reservas = []
    
    
    
    def registrar_reserva(self, producto_id, cantidad):
        reserva = {
            "producto_id": producto_id,
            "cantidad": cantidad
        }
        self.reservas.append(reserva)