"""Capa de Entidades: representa un registro de la tabla Productos."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Producto:
    
    nombre: str
    categoria: str
    precio: float
    stock: int
    id_producto: Optional[int] = None

    def __str__(self):
        return self.nombre
