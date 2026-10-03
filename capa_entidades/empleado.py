"""Capa de Entidades: representa un registro de la tabla Empleados."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Empleado:
    nombre: str
    documento: str = ""
    direccion: str = ""
    telefono: str = ""
    email: str = ""
    id_empleado: Optional[int] = None

    def __str__(self):
        return self.nombre
