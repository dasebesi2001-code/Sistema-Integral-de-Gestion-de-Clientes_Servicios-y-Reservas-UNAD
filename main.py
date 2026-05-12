import logging
from servicios_gestion import cliente, registro_reservas
from servicio_modelos import alquilerEquipo, reservas_de_Salas, asesoramiento
from servicios_excepeciones import ValidacionError, ProyectoError

logging.basicConfig(
    filename='gestion_software_FJ.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    gestor=registro_reservas()
    cliente1=cliente(10056, "Daniel Benavides", "daniel.benavides@example.com")
    cliente2=cliente(20625, "Maria Gomez", "maria.gomez@example.com")
    cliente3=cliente(30456, "Gabriela Calderon", "gabriela.calderon@example.com")
    
    print("----------INICIO DE PRUEBAS-------")
    

if __name__ == "__main__":
        main()