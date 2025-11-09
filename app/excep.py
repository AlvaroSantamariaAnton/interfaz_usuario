# Módulo que define excepciones personalizadas utilizadas en la aplicación


class MenorEdadError(Exception):
    """
    Excepción lanzada cuando un usuario intenta registrarse o acceder
    siendo menor de edad.
    """
    pass


class UsuarioBloqueadoError(Exception):
    """
    Excepción lanzada cuando un usuario intenta iniciar sesión
    pero su cuenta está bloqueada por el administrador.
    """
    pass
