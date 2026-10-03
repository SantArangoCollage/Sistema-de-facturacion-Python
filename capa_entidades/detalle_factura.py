"""Capa de Entidades: un renglón del detalle de una factura."""
from dataclasses import dataclass
from typing import Optional

from capa_entidades.producto import Producto


@dataclass
class DetalleFactura:
    producto: Producto
    cantidad: int
    precio: float
    id_detalle: Optional[int] = None

    @property
    def subtotal(self) -> float:
        return self.cantidad * self.precio
