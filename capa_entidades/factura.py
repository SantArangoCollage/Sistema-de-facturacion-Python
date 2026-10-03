"""Capa de Entidades: representa un registro de la tabla Facturas
(encabezado) junto con sus líneas de detalle."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from capa_entidades.cliente import Cliente
from capa_entidades.detalle_factura import DetalleFactura
from capa_entidades.empleado import Empleado


@dataclass
class Factura:
    cliente: Optional[Cliente] = None
    empleado: Optional[Empleado] = None
    fecha_registro: datetime = field(default_factory=datetime.now)
    estado: str = "Pendiente"
    descuento: float = 0.0
    iva: float = 0.0
    detalles: List[DetalleFactura] = field(default_factory=list)
    id_factura: Optional[int] = None

    @property
    def subtotal(self) -> float:
        return sum(d.subtotal for d in self.detalles)

    @property
    def total_factura(self) -> float:
        return self.subtotal - self.descuento + self.iva
