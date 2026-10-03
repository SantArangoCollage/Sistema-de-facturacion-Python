"""Capa de Entidades: representa un registro de la tabla Clientes."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    nombre: str
    documento: str = ""
    direccion: str = ""
    telefono: str = ""
    email: str = ""
    id_cliente: Optional[int] = None

    def __str__(self):
        return self.nombre
