"""
Modelos de datos que siguen en memoria (no en SQL Server).

Solo queda Categoria: Empleado, Usuario, Cliente, Producto, Factura y
DetalleFactura ahora viven en la Capa de Entidades (capa_entidades/),
porque todas esas tablas ya están conectadas a SQL Server con su
arquitectura por capas completa.
"""
from dataclasses import dataclass


@dataclass
class Categoria:
    nombre: str
    descripcion: str = ""

    def __str__(self):
        return self.nombre
