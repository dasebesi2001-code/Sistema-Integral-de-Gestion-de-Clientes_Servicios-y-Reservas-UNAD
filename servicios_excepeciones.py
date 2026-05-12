import logging
class ProyectoError(Exception):
    """clase base para las excepciones en este módulo."""
    pass    


class elemento_no_encontrado(ProyectoError):
    """se lanza cuando no se encuentra un elemento específico en la base de datos o en la colección."""
    pass

class ValidacionError(ProyectoError):
    """se lanza cuando se produce un error de validación en los datos de entrada."""
    pass