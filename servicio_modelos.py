
import json
import os 
from abc import ABC, abstractmethod 
class servicio(ABC):
    def __init__(self, id, nombre, precio, cantidad):
        self.__id = id
        self.__nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        raise AttributeError("El ID no se puede modificar después de la creación del producto.")    
    @abstractmethod
    def calcular_costo_total(self):
        pass

class alquilerEquipo(servicio):
    def __init__(self, id, nombre, precio, cantidad, duracion):
        super().__init__(id, nombre, precio, cantidad)
        self.duracion = duracion
        if self.duracion <= 0:
            raise ValueError("La duración del alquiler debe ser mayor que cero.")
        elif self.duracion > 2:
            raise ValueError("La duración del alquiler no puede ser mayor que dos días.")
    def calcular_costo_total(self):
        alquiler_total = self.precio * self.duracion       
        return alquiler_total
        
      
class alquiler_equipos(servicio):
    def __init__(self, id, nombre, precio, cantidad, duracion):
        super().__init__(id, nombre, precio, cantidad)
        self.duracion = duracion
        if self.duracion <= 0:
            raise ValueError("La duración del alquiler debe ser mayor que cero.")  
        elif self.duracion > 24:
            raise ValueError("La duración del alquiler no puede ser mayor que 24 horas.")
    def calcular_costo_total(self):
        alquiler_total = self.precio * self.duracion       
        return alquiler_total
        
class asesoramiento(servicio):
    def __init__(self, id, nombre, precio, tipo):
        super().__init__(id, nombre, precio)
        self.tipo = tipo

    def calcular_costo_total(self):
        tarifas = {
            "técnico": 100000,
            "estratégico": 150000,
            "táctico": 100000,
            "operativo": 120000
        }
        
        # .get() busca el tipo; si no existe, usa 0 por defecto
        recargo = tarifas.get(self.tipo.lower(), 0)
        
        # El total sería el precio base más el recargo del tipo
        return (self.precio + recargo) 
    
    
    