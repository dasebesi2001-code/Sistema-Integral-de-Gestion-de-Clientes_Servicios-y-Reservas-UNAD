"""
servicios_gestion.py
Gestión de reservas y clientes del Sistema Software FJ.
Clases:
  - reservas         (integra cliente, servicio, fecha y estado)
  - registro_reservas(gestiona la lista de reservas con manejo de excepciones)
Universidad Nacional Abierta y a Distancia - UNAD
Curso: Programación 213023
"""
#Propuesta de cambio y reorganizacion de codigo - Jesus Solis
""""
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
            """

import logging
from datetime import datetime
from servicio_modelos import cliente, servicio, EntidadBase
from servicios_excepeciones import (
    ValidacionError,
    ProyectoError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoCostoError,
    ClienteInvalidoError,
    elemento_no_encontrado,
)
 
# ---------------------------------------------------------------------------
# Configuración del logger
# ---------------------------------------------------------------------------
logging.basicConfig(
    filename='errores_sistemas.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
 
# ===========================================================================
# CLASE RESERVAS
# ===========================================================================
 
class reservas:
    """
    Representa una reserva de servicio para un cliente.
    Ciclo de vida: PENDIENTE → CONFIRMADA → PROCESADA | CANCELADA
    """
 
    def __init__(self, id_reservas, cliente_obj: cliente,
                 servicio_obj: servicio, fecha_reserva: str):
        # Validar tipos
        if not isinstance(cliente_obj, cliente):
            raise ReservaInvalidaError("Se requiere un objeto cliente válido.")
        if not isinstance(servicio_obj, servicio):
            raise ReservaInvalidaError("Se requiere un objeto servicio válido.")
 
        self.__id_reservas  = id_reservas
        self.cliente        = cliente_obj
        self.servicio       = servicio_obj
        self._fecha_reserva = fecha_reserva
        self.estado         = "pendiente"
        self._costo_total   = 0.0
        self._historial     = [
            f"[{self._timestamp()}] Reserva creada en estado PENDIENTE."
        ]
 
    @property
    def id_reservas(self):
        return self.__id_reservas
 
    @property
    def costo_total(self) -> float:
        return self._costo_total
 
    def _timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
    # ---- Ciclo de vida ----
 
    def procesar_confirmacion(self, descuento: float = 0.0,
                              aplicar_iva: bool = True) -> float:
        """
        Confirma la reserva calculando el costo final.
        Usa try/except/else/finally.
        """
        try:
            if self.estado != "pendiente":
                raise OperacionNoPermitidaError(
                    f"Solo se puede confirmar una reserva en estado PENDIENTE. "
                    f"Estado actual: {self.estado}"
                )
            if not self.cliente.activo:
                raise ReservaInvalidaError(
                    f"El cliente '{self.cliente.nombre}' no está activo."
                )
            # Verificar disponibilidad del servicio
            self.servicio._verificar_disponibilidad()
 
            # Calcular costo con variante completa (método sobrecargado)
            self._costo_total = self.servicio.calcular_costo_final(
                descuento=descuento, aplicar_iva=aplicar_iva
            )
 
        except (OperacionNoPermitidaError, ReservaInvalidaError, CalculoCostoError):
            raise  # Re-lanzar excepciones del dominio sin modificar
 
        except ProyectoError as e:
            # Encadenamiento: cualquier otra excepción propia se envuelve
            raise ReservaInvalidaError(
                f"Error al confirmar la reserva {self.__id_reservas}: {e}"
            ) from e
 
        except Exception as e:
            # Encadenamiento para errores inesperados
            raise ReservaInvalidaError(
                f"Error inesperado al confirmar reserva {self.__id_reservas}: {e}"
            ) from e
 
        else:
            # Solo se ejecuta si NO hubo excepción
            self.estado = "confirmada"
            self._historial.append(
                f"[{self._timestamp()}] Reserva CONFIRMADA. "
                f"Costo: ${self._costo_total:,.2f} "
                f"(descuento={descuento*100:.0f}%, IVA={'sí' if aplicar_iva else 'no'})"
            )
            return self._costo_total
 
        finally:
            # Siempre se ejecuta: aquí iría liberación de recursos o auditoría
            pass
 
    def cancelar(self, motivo: str = "Sin motivo especificado"):
        """
        Cancela la reserva si está en estado pendiente o confirmada.
        Usa try/except/finally.
        """
        try:
            if self.estado in ("procesada", "cancelada"):
                raise OperacionNoPermitidaError(
                    f"No se puede cancelar una reserva en estado '{self.estado}'."
                )
        except OperacionNoPermitidaError:
            raise
        finally:
            pass  # finally requerido
 
        self.estado       = "cancelada"
        self._costo_total = 0.0
        self._historial.append(
            f"[{self._timestamp()}] Reserva CANCELADA. Motivo: {motivo}"
        )
 
    def procesar(self):
        """
        Marca la reserva como procesada (ejecutada).
        Usa try/except/finally.
        """
        try:
            if self.estado != "confirmada":
                raise OperacionNoPermitidaError(
                    f"Solo se pueden procesar reservas CONFIRMADAS. "
                    f"Estado actual: {self.estado}"
                )
            if self._costo_total <= 0:
                raise CalculoCostoError(
                    f"El costo de la reserva {self.__id_reservas} es inválido."
                )
        except (OperacionNoPermitidaError, CalculoCostoError):
            raise
        except Exception as e:
            raise ReservaInvalidaError(
                f"Error inesperado al procesar reserva {self.__id_reservas}."
            ) from e
        finally:
            pass
 
        self.estado = "procesada"
        self._historial.append(
            f"[{self._timestamp()}] Reserva PROCESADA exitosamente."
        )
 
    def historial(self) -> str:
        return "\n  ".join(self._historial)
 
    def __str__(self) -> str:
        return (
            f"\nReserva [ID:{self.__id_reservas}]"
            f"\n  Cliente : {self.cliente.nombre} (ID:{self.cliente.id})"
            f"\n  Servicio: {self.servicio.nombre} (ID:{self.servicio.id})"
            f"\n  Fecha   : {self._fecha_reserva}"
            f"\n  Estado  : {self.estado.upper()}"
            f"\n  Costo   : ${self._costo_total:,.2f}"
            f"\n  Historial:\n  {self.historial()}"
        )
 
 
# ===========================================================================
# CLASE REGISTRO_RESERVAS (gestiona la lista de reservas)
# ===========================================================================
 
class registro_reservas:
    """
    Gestiona el registro y consulta de todas las reservas del sistema.
    """
 
    def __init__(self):
        self.reservas_lista = []  # Lista interna de objetos reservas
 
    def agregar_reserva(self, id_reserva, cliente_obj: cliente,
                        servicio_obj: servicio, fecha_reserva: str,
                        descuento: float = 0.0, aplicar_iva: bool = True):
        """
        Crea y confirma una reserva. Maneja y registra todas las excepciones.
        Retorna el costo si fue exitosa, o un mensaje de error controlado.
        """
        try:
            if not isinstance(servicio_obj, servicio):
                raise ValidacionError("El servicio proporcionado no es válido.")
            nueva = reservas(id_reserva, cliente_obj, servicio_obj, fecha_reserva)
            costo = nueva.procesar_confirmacion(
                descuento=descuento, aplicar_iva=aplicar_iva
            )
            self.reservas_lista.append(nueva)
            return costo
 
        except ProyectoError as e:
            logging.error(
                f"Error al agregar reserva: id_reserva={id_reserva} | {e}"
            )
            return f"Error controlado: {e}"
 
        except Exception as e:
            logging.error(
                f"Error inesperado al agregar reserva: id_reserva={id_reserva} | {e}"
            )
            return "Error inesperado al agregar reserva. Inténtelo de nuevo más tarde."
 
    def cancelar_reserva(self, id_reserva, motivo: str = "Sin motivo"):
        """Busca y cancela una reserva por su ID."""
        try:
            res = self._buscar_reserva(id_reserva)
            res.cancelar(motivo)
            return f"Reserva {id_reserva} cancelada correctamente."
        except ProyectoError as e:
            logging.error(f"Error al cancelar reserva {id_reserva}: {e}")
            return f"Error controlado: {e}"
 
    def procesar_reserva(self, id_reserva):
        """Busca y procesa una reserva confirmada."""
        try:
            res = self._buscar_reserva(id_reserva)
            res.procesar()
            return f"Reserva {id_reserva} procesada correctamente."
        except ProyectoError as e:
            logging.error(f"Error al procesar reserva {id_reserva}: {e}")
            return f"Error controlado: {e}"
 
    def _buscar_reserva(self, id_reserva) -> reservas:
        """Busca una reserva por ID; lanza elemento_no_encontrado si no existe."""
        for r in self.reservas_lista:
            if r.id_reservas == id_reserva:
                return r
        raise elemento_no_encontrado(
            f"No se encontró ninguna reserva con ID: {id_reserva}"
        )
 
    def listar_reservas(self):
        """Imprime todas las reservas registradas."""
        if not self.reservas_lista:
            print("  No hay reservas registradas.")
            return
        for r in self.reservas_lista:
            print(r)