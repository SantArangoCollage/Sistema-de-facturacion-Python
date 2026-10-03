"""Datos de la sesión activa."""
from typing import Optional


class Sesion:
    id_usuario: Optional[int] = None
    usuario: Optional[str] = None
    nombre: Optional[str] = None
    rol: Optional[str] = None

    @classmethod
    def cerrar(cls) -> None:
        cls.id_usuario = None
        cls.usuario = None
        cls.nombre = None
        cls.rol = None
