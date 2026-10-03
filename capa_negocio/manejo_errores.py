"""
Capa de Negocio: manejo de excepciones de base de datos.

'contexto_bd' es un context manager: envuelve la llamada a la Capa de
Datos y, si truena con ErrorBaseDatos, la vuelve a lanzar con un
mensaje de contexto al inicio, conservando el detalle técnico original
(gracias a 'from ex', como ya hace acceso_datos.py).
"""
from contextlib import contextmanager

from acceso_datos import ErrorBaseDatos


@contextmanager
def contexto_bd(mensaje: str):
    try:
        yield
    except ErrorBaseDatos as ex:
        raise ErrorBaseDatos(f"{mensaje}: {ex}") from ex
