"""
servicio_modelos.py
Modelos del sistema Software FJ:
  - EntidadBase      (clase abstracta general del sistema)
  - cliente          (con encapsulación y validaciones robustas)
  - servicio         (clase abstracta con métodos sobrecargados de costo)
  - alquilerEquipo   (hereda de servicio)
  - reservas_de_Salas(hereda de servicio)
  - asesoramiento    (hereda de servicio)
Universidad Nacional Abierta y a Distancia - UNAD
Curso: Programación 213023
"""

#Propuesta de codigo - Jesus Solis
""""
from abc import ABC, abstractmethod 
from servicios_excepeciones import ValidacionError, ProyectoError

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
        raise ValidacionError("El ID no se puede modificar después de la creación del producto.")    
    @abstractmethod
    def calcular_costo_total(self):
        pass

class alquilerEquipo(servicio):
    def __init__(self, id, nombre, precio, cantidad, duracion):
        super().__init__(id, nombre, precio, cantidad)
        self.duracion = duracion
        if self.duracion <= 0:
            raise ValidacionError("La duración del alquiler debe ser mayor que cero.")
        elif self.duracion > 2:
            raise ValidacionError("La duración del alquiler no puede ser mayor que dos días.")
    def calcular_costo_total(self):
        alquiler_total = self.precio * self.duracion       
        return alquiler_total
        
      
class reservas_de_Salas (servicio):
    def __init__(self, id, nombre, precio, cantidad, duracion):
        super().__init__(id, nombre, precio, cantidad)
        self.duracion = duracion
        if self.duracion <= 0:
            raise ValidacionError("La duración del alquiler debe ser mayor que cero.")  
        elif self.duracion > 24:
            raise ValidacionError("La duración del alquiler no puede ser mayor que 24 horas.")
    def calcular_costo_total(self):
        alquiler_total = self.precio * self.duracion       
        return alquiler_total
        
class asesoramiento(servicio):
    def __init__(self, id, nombre, precio, tipo, cantidad):
        super().__init__(id, nombre, precio, cantidad)
        self.tipo = tipo

    def calcular_costo_total(self):
        tarifas = {
            "técnico": 100000,
            "estratégico": 150000,
            "táctico": 100000,
            "operativo": 120000
        }
        
        # selecciona el recargo basado en el tipo de asesoramiento, si el tipo no está en las tarifas, se asume un recargo de 0
        recargo = tarifas.get(self.tipo.lower(), 0)
        
        # El total sería el precio base más el recargo del tipo
        return (self.precio + recargo)* self.cantidad 
    """
    
import re
import logging
from abc import ABC, abstractmethod
from servicios_excepeciones import (
    ValidacionError,
    ProyectoError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    DuracionInvalidaError,
    CalculoCostoError,
)
 
 
# ===========================================================================
# CLASE ABSTRACTA BASE (representa entidades generales del sistema)
# ===========================================================================
 
class EntidadBase(ABC):
    """
    Clase abstracta que representa cualquier entidad del sistema Software FJ.
    Garantiza que todas las entidades tengan descripción y validación.
    """
 
    def __init__(self, id):
        self._id = id
 
    @property
    def id(self):
        return self._id
 
    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción textual de la entidad."""
        pass
 
    @abstractmethod
    def validar(self) -> bool:
        """Valida que los datos de la entidad sean consistentes."""
        pass
 
    def __str__(self):
        return self.describir()
 
 
# ===========================================================================
# CLASE CLIENTE (hereda de EntidadBase)
# ===========================================================================
 
class cliente(EntidadBase):
    """
    Representa un cliente de Software FJ.
    Encapsula datos personales con validaciones estrictas.
    """
 
    def __init__(self, id, nombre: str, correo: str, telefono: str = ""):
        super().__init__(id)
        # Usamos setters para validar desde el constructor
        self.nombre   = nombre
        self.correo   = correo
        self.telefono = telefono
        self._activo  = True
 
    # ---- Propiedades con encapsulación ----
 
    @property
    def nombre(self) -> str:
        return self._nombre
 
    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                f"El nombre '{valor}' no es válido. Debe tener al menos 3 caracteres."
            )
        if not re.match(r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$", valor.strip()):
            raise ClienteInvalidoError("El nombre solo puede contener letras y espacios.")
        self._nombre = valor.strip()
 
    @property
    def correo(self) -> str:
        return self._correo
 
    @correo.setter
    def correo(self, valor: str):
        if not valor or not isinstance(valor, str):
            raise ClienteInvalidoError("El correo no puede estar vacío.")
        valor = valor.strip().lower()
        if not re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$", valor):
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self._correo = valor
 
    @property
    def telefono(self) -> str:
        return self._telefono
 
    @telefono.setter
    def telefono(self, valor: str):
        # El teléfono es opcional; si se proporciona se valida
        if valor == "" or valor is None:
            self._telefono = ""
            return
        valor = str(valor).strip().replace(" ", "").replace("-", "")
        if not valor.lstrip("+").isdigit() or len(valor.lstrip("+")) < 7:
            raise ClienteInvalidoError(
                f"El teléfono '{valor}' no es válido. Debe tener al menos 7 dígitos."
            )
        self._telefono = valor
 
    @property
    def activo(self) -> bool:
        return self._activo
 
    def desactivar(self):
        self._activo = False
 
    # ---- Métodos abstractos implementados ----
 
    def describir(self) -> str:
        estado = "Activo" if self._activo else "Inactivo"
        tel = f" | Tel: {self._telefono}" if self._telefono else ""
        return (
            f"Cliente [ID:{self._id}] | Nombre: {self._nombre} "
            f"| Correo: {self._correo}{tel} | Estado: {estado}"
        )
 
    def validar(self) -> bool:
        return bool(self._nombre and self._correo and self._activo)
 
 
# ===========================================================================
# CLASE ABSTRACTA SERVICIO (hereda de EntidadBase)
# ===========================================================================
 
class servicio(EntidadBase):
    """
    Clase abstracta que representa un servicio ofrecido por Software FJ.
    Define la interfaz común e implementa métodos sobrecargados de costo.
    """
 
    TARIFA_IVA = 0.19  # 19%
 
    def __init__(self, id, nombre: str, precio: float, cantidad: int):
        super().__init__(id)
        self.__nombre   = nombre
        self.precio     = precio
        self.cantidad   = cantidad
        self._disponible = True
 
    # ---- Propiedad nombre (solo lectura) ----
    @property
    def nombre(self) -> str:
        return self.__nombre
 
    # ---- Propiedad id (heredada, con setter bloqueado) ----
    @EntidadBase.id.setter
    def id(self, value):
        raise ValidacionError("El ID no se puede modificar después de la creación del servicio.")
 
    # ---- Propiedad precio con validación ----
    @property
    def precio(self) -> float:
        return self._precio
 
    @precio.setter
    def precio(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ServicioInvalidoError(
                f"El precio debe ser un número positivo. Se recibió: {valor}"
            )
        self._precio = float(valor)
 
    # ---- Disponibilidad ----
    @property
    def disponible(self) -> bool:
        return self._disponible
 
    def habilitar(self):
        self._disponible = True
 
    def deshabilitar(self):
        self._disponible = False
 
    def _verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(self.__nombre)
 
    # ---- Método abstracto principal ----
    @abstractmethod
    def calcular_costo_total(self) -> float:
        """Calcula el costo base del servicio."""
        pass
 
    # ---- Métodos sobrecargados de costo ----
 
    def calcular_costo_con_iva(self) -> float:
        """Variante 1: costo base + IVA del 19%."""
        costo = self.calcular_costo_total()
        return round(costo * (1 + self.TARIFA_IVA), 2)
 
    def calcular_costo_con_descuento(self, descuento: float = 0.0) -> float:
        """Variante 2: costo base con porcentaje de descuento."""
        if not (0.0 <= descuento <= 1.0):
            raise CalculoCostoError(
                f"El descuento debe estar entre 0 y 1. Se recibió: {descuento}"
            )
        costo = self.calcular_costo_total()
        return round(costo * (1 - descuento), 2)
 
    def calcular_costo_final(self, descuento: float = 0.0,
                             aplicar_iva: bool = True) -> float:
        """
        Variante 3 (completa): costo base → descuento → IVA opcional.
        Parámetros opcionales permiten cualquier combinación.
        """
        costo = self.calcular_costo_con_descuento(descuento)
        if aplicar_iva:
            costo = round(costo * (1 + self.TARIFA_IVA), 2)
        return costo
 
    # ---- Métodos abstractos de EntidadBase ----
 
    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"Servicio [ID:{self._id}] '{self.__nombre}' | "
            f"Precio: ${self._precio:,.0f} | Cantidad: {self.cantidad} | Estado: {estado}"
        )
 
    def validar(self) -> bool:
        return self._disponible and self._precio > 0
 
 
# ===========================================================================
# SERVICIO 1: ALQUILER DE EQUIPO
# ===========================================================================
 
class alquilerEquipo(servicio):
    """Servicio de alquiler de equipos tecnológicos."""
 
    TIPOS_VALIDOS = {"computador", "proyector", "camara", "tablet", "servidor"}
 
    def __init__(self, id, nombre: str, precio: float, cantidad: int,
                 duracion: float, tipo_equipo: str = "computador"):
        super().__init__(id, nombre, precio, cantidad)
        tipo_lower = tipo_equipo.strip().lower()
        if tipo_lower not in self.TIPOS_VALIDOS:
            raise ServicioInvalidoError(
                f"Tipo de equipo '{tipo_equipo}' no válido. "
                f"Tipos permitidos: {', '.join(self.TIPOS_VALIDOS)}"
            )
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DuracionInvalidaError(duracion, 0.5, 2)
        if duracion > 2:
            raise DuracionInvalidaError(duracion, 0.5, 2)
        self.duracion    = duracion
        self.tipo_equipo = tipo_lower
 
    def calcular_costo_total(self) -> float:
        """Costo base: precio × duración, con descuento por volumen de días."""
        factor = 0.90 if self.duracion >= 1.5 else 1.0
        return round(self.precio * self.duracion * self.cantidad * factor, 2)
 
    def describir(self) -> str:
        return (
            super().describir()
            + f" | Tipo: {self.tipo_equipo.capitalize()} | Duración: {self.duracion} día(s)"
        )
 
 
# ===========================================================================
# SERVICIO 2: RESERVA DE SALAS
# ===========================================================================
 
class reservas_de_Salas(servicio):
    """Servicio de reserva de salas de reunión o conferencia."""
 
    def __init__(self, id, nombre: str, precio: float, cantidad: int,
                 duracion: float, capacidad: int = 10):
        super().__init__(id, nombre, precio, cantidad)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(
                f"La capacidad debe ser un entero positivo. Se recibió: {capacidad}"
            )
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DuracionInvalidaError(duracion, 1, 24)
        if duracion > 24:
            raise DuracionInvalidaError(duracion, 1, 24)
        self.duracion  = duracion
        self.capacidad = capacidad
 
    def calcular_costo_total(self) -> float:
        """Costo base: precio × duración, con recargo si duración supera 12h."""
        factor = 1.15 if self.duracion > 12 else 1.0
        return round(self.precio * self.duracion * self.cantidad * factor, 2)
 
    def describir(self) -> str:
        return (
            super().describir()
            + f" | Capacidad: {self.capacidad} personas | Duración: {self.duracion}h"
        )
 
 
# ===========================================================================
# SERVICIO 3: ASESORAMIENTO
# ===========================================================================
 
class asesoramiento(servicio):
    """Servicio de asesoría especializada."""
 
    TARIFAS_TIPO = {
        "técnico":     100_000,
        "estratégico": 150_000,
        "táctico":     100_000,
        "operativo":   120_000,
    }
 
    def __init__(self, id, nombre: str, precio: float, tipo: str, cantidad: int,
                 asesor: str = "Por asignar"):
        tipos_validos = set(self.TARIFAS_TIPO.keys())
        if tipo.lower() not in tipos_validos:
            raise ServicioInvalidoError(
                f"Tipo de asesoría '{tipo}' no válido. "
                f"Tipos permitidos: {', '.join(tipos_validos)}"
            )
        super().__init__(id, nombre, precio, cantidad)
        self.tipo   = tipo.lower()
        self.asesor = asesor
 
    def calcular_costo_total(self) -> float:
        """Precio base + recargo según tipo × cantidad."""
        recargo = self.TARIFAS_TIPO.get(self.tipo, 0)
        return round((self.precio + recargo) * self.cantidad, 2)
 
    def describir(self) -> str:
        return (
            super().describir()
            + f" | Tipo asesoría: {self.tipo.capitalize()} | Asesor: {self.asesor}"
        )