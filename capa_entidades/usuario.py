"""Capa de Entidades."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    nombre: str
    login: str
    clave: str
    rol: str
    id_usuario: Optional[int] = None
