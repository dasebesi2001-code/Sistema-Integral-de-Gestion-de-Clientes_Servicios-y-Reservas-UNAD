
import json
import os 

class Producto:
    def __init__(self, id, nombre, precio, cantidad):
        self._id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        raise AttributeError("El ID no se puede modificar después de la creación del producto.")    
    
    