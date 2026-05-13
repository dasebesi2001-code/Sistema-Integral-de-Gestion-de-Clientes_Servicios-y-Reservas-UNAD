"""
main.py
Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ
Universidad Nacional Abierta y a Distancia - UNAD
Curso: Programación 213023
 
Simula 13 operaciones completas (válidas e inválidas), incluyendo los
clientes originales del repositorio: Daniel Benavides, Maria Gomez
y Gabriela Calderon.
"""

import logging
from servicios_gestion import cliente, registro_reservas, reservas
from servicio_modelos import alquilerEquipo, reservas_de_Salas, asesoramiento
from servicios_excepeciones import ValidacionError, ProyectoError


logging.basicConfig(
    filename='gestion_software_FJ.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


#Cambio estructura - Jesus Solis
"""""
def main():
    gestor=registro_reservas()
    cliente1=cliente(10056, "Daniel Benavides", "daniel.benavides@example.com")
    cliente2=cliente(20625, "Maria Gomez", "maria.gomez@example.com")
    cliente3=cliente(30456, "Gabriela Calderon", "gabriela.calderon@example.com")
    
        print("----------INICIO DE PRUEBAS-------")
        
        if __name__ == "__main__":
        main()
        """

def separador(titulo: str):
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")
    
def main():
    gestor = registro_reservas()
 
    # -----------------------------------------------------------------------
    # Clientes originales del repositorio + uno adicional
    # -----------------------------------------------------------------------
    separador("REGISTRO DE CLIENTES")
 
    # OP 1 — Clientes válidos (los 3 originales)
    try:
        cliente1 = cliente(10056, "Daniel Benavides",
                           "daniel.benavides@example.com", "3101234567")
        cliente2 = cliente(20625, "Maria Gomez",
                           "maria.gomez@example.com", "3209876543")
        cliente3 = cliente(30456, "Gabriela Calderon",
                           "gabriela.calderon@example.com", "3151112233")
        print(f"  ✓ {cliente1.describir()}")
        print(f"  ✓ {cliente2.describir()}")
        print(f"  ✓ {cliente3.describir()}")
    except ProyectoError as e:
        logging.error(f"Error al registrar clientes: {e}")
        print(f"  ✗ Error: {e}")
 
    # OP 2 — Cliente con correo inválido (error esperado)
    separador("OP 2 - Cliente con correo inválido")
    try:
        cliente_malo = cliente(99999, "Juan Sin Correo", "correo_invalido", "")
    except ProyectoError as e:
        logging.error(f"Error esperado - correo inválido: {e}")
        print(f"  ✗ Error esperado: {e}")
 
    # OP 3 — Cliente con nombre muy corto (error esperado)
    separador("OP 3 - Cliente con nombre muy corto")
    try:
        cliente_malo2 = cliente(88888, "Jo", "jo@test.com", "")
    except ProyectoError as e:
        logging.error(f"Error esperado - nombre corto: {e}")
        print(f"  ✗ Error esperado: {e}")
 
    # -----------------------------------------------------------------------
    # Creación de servicios
    # -----------------------------------------------------------------------
    separador("OP 4 - Crear servicios válidos")
    try:
        equipo1 = alquilerEquipo(
            id=1, nombre="Computador Dell XPS", precio=80_000,
            cantidad=1, duracion=1.5, tipo_equipo="computador"
        )
        sala1 = reservas_de_Salas(
            id=2, nombre="Sala Innovación", precio=50_000,
            cantidad=1, duracion=3, capacidad=10
        )
        asesoria1 = asesoramiento(
            id=3, nombre="Asesoría Técnica", precio=120_000,
            tipo="técnico", cantidad=1, asesor="Ing. Laura Ríos"
        )
        print(f"  ✓ {equipo1.describir()}")
        print(f"  ✓ {sala1.describir()}")
        print(f"  ✓ {asesoria1.describir()}")
    except ProyectoError as e:
        logging.error(f"Error al crear servicios: {e}")
        print(f"  ✗ Error: {e}")
 
    # OP 5 — Equipo con tipo inválido (error esperado)
    separador("OP 5 - Equipo con tipo inválido")
    try:
        equipo_malo = alquilerEquipo(
            id=99, nombre="Dron ilegal", precio=50_000,
            cantidad=1, duracion=1, tipo_equipo="dron"
        )
    except ProyectoError as e:
        logging.error(f"Error esperado - tipo equipo inválido: {e}")
        print(f"  ✗ Error esperado: {e}")
 
    # OP 6 — Servicio con precio negativo (error esperado)
    separador("OP 6 - Servicio con precio negativo")
    try:
        sala_mala = reservas_de_Salas(
            id=98, nombre="Sala Inválida", precio=-5000,
            cantidad=1, duracion=2
        )
    except ProyectoError as e:
        logging.error(f"Error esperado - precio negativo: {e}")
        print(f"  ✗ Error esperado: {e}")
 
    # -----------------------------------------------------------------------
    # Operaciones de reserva
    # -----------------------------------------------------------------------
 
    # OP 7 — Reserva exitosa: Daniel reserva el equipo
    separador("OP 7 - Reserva exitosa (Daniel - Equipo)")
    resultado = gestor.agregar_reserva(
        id_reserva=1001, cliente_obj=cliente1,
        servicio_obj=equipo1, fecha_reserva="2025-06-10",
        descuento=0.10, aplicar_iva=True
    )
    print(f"  ✓ Costo final: ${resultado:,.2f}" if isinstance(resultado, float)
          else f"  ✗ {resultado}")
 
    # OP 8 — Reserva exitosa: Maria reserva la sala
    separador("OP 8 - Reserva exitosa (Maria - Sala)")
    resultado2 = gestor.agregar_reserva(
        id_reserva=1002, cliente_obj=cliente2,
        servicio_obj=sala1, fecha_reserva="2025-06-11",
        descuento=0.0, aplicar_iva=True
    )
    print(f"  ✓ Costo final: ${resultado2:,.2f}" if isinstance(resultado2, float)
          else f"  ✗ {resultado2}")
 
    # OP 9 — Reserva exitosa: Gabriela reserva asesoría
    separador("OP 9 - Reserva exitosa (Gabriela - Asesoría)")
    resultado3 = gestor.agregar_reserva(
        id_reserva=1003, cliente_obj=cliente3,
        servicio_obj=asesoria1, fecha_reserva="2025-06-12",
        descuento=0.05, aplicar_iva=True
    )
    print(f"  ✓ Costo final: ${resultado3:,.2f}" if isinstance(resultado3, float)
          else f"  ✗ {resultado3}")
 
    # OP 10 — Procesar reserva de Daniel
    separador("OP 10 - Procesar reserva de Daniel")
    msg = gestor.procesar_reserva(1001)
    print(f"  ✓ {msg}")
 
    # OP 11 — Cancelar reserva de Maria (permitido: está confirmada)
    separador("OP 11 - Cancelar reserva de Maria")
    msg2 = gestor.cancelar_reserva(1002, "Cliente solicitó reprogramación")
    print(f"  ✓ {msg2}")
 
    # OP 12 — Intentar cancelar la reserva de Daniel ya PROCESADA (error esperado)
    separador("OP 12 - Cancelar reserva ya procesada (error esperado)")
    msg3 = gestor.cancelar_reserva(1001, "Intento inválido")
    print(f"  ✗ {msg3}")
 
    # OP 13 — Servicio no disponible (error esperado)
    separador("OP 13 - Reserva con servicio deshabilitado")
    try:
        asesoria1.deshabilitar()
        print(f"  Servicio deshabilitado: {asesoria1.nombre}")
        resultado4 = gestor.agregar_reserva(
            id_reserva=1004, cliente_obj=cliente3,
            servicio_obj=asesoria1, fecha_reserva="2025-06-13"
        )
        print(f"  ✗ {resultado4}")
    finally:
        asesoria1.habilitar()
        print(f"  Servicio rehabilitado: {asesoria1.nombre}")
 
    # OP 14 — Mostrar variantes de costo del servicio de sala (métodos sobrecargados)
    separador("OP 14 - Variantes de cálculo de costo (sala1)")
    try:
        base     = sala1.calcular_costo_total()
        con_iva  = sala1.calcular_costo_con_iva()
        con_desc = sala1.calcular_costo_con_descuento(descuento=0.15)
        final    = sala1.calcular_costo_final(descuento=0.15, aplicar_iva=True)
        print(f"  Costo base              : ${base:>12,.2f}")
        print(f"  Con IVA (19%)           : ${con_iva:>12,.2f}")
        print(f"  Con descuento 15%       : ${con_desc:>12,.2f}")
        print(f"  Total (desc 15% + IVA)  : ${final:>12,.2f}")
    except ProyectoError as e:
        logging.error(f"Error en cálculo de costos: {e}")
        print(f"  ✗ {e}")
 
    # -----------------------------------------------------------------------
    # Resumen de todas las reservas
    # -----------------------------------------------------------------------
    separador("RESUMEN DE RESERVAS REGISTRADAS")
    gestor.listar_reservas()
 
    separador("SIMULACIÓN COMPLETADA")
    print("  Revise 'errores_sistemas.log' y 'gestion_software_FJ.log'")
    print("  para el detalle completo de errores registrados.")
 
 
if __name__ == "__main__":
    print("=" * 60)
    print("  SISTEMA SOFTWARE FJ - INICIO")
    print("=" * 60)
    main()