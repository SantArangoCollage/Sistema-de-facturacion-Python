"""
Capa de Datos: acceso a las tablas Facturas y DetalleFactura en SQL
Server.

Una factura son en realidad DOS tablas: el encabezado (Facturas) y sus
líneas (DetalleFactura, una fila por producto agregado). Por eso esta
clase, a diferencia de ClienteDatos/ProductoDatos/EmpleadoDatos, tiene
un método extra ('consultar_detalle') y su 'insertar' hace dos pasos:
primero guarda el encabezado y obtiene su IdFactura recién generado
(con 'ejecutar_insert_devolviendo_id'), y luego guarda cada línea de
detalle con ese IdFactura.
"""
from typing import List

from acceso_datos import AccesoDatos
from capa_entidades.factura import Factura


class FacturaDatos:
    def __init__(self):
        self.acceso_datos = AccesoDatos()

    def consultar_todas(self) -> List[dict]:
        """Una fila por factura, con el nombre de cliente/empleado ya
        resueltos (JOIN) y el subtotal ya sumado desde DetalleFactura."""
        sql = """
            SELECT
                f.IdFactura,
                f.IdCliente,
                c.Nombre AS ClienteNombre,
                f.IdEmpleado,
                e.Nombre AS EmpleadoNombre,
                f.FechaRegistro,
                f.Estado,
                f.Descuento,
                f.Iva,
                ISNULL(SUM(d.Cantidad * d.Precio), 0) AS Subtotal
            FROM Facturas f
            LEFT JOIN Clientes c ON c.IdCliente = f.IdCliente
            LEFT JOIN Empleados e ON e.IdEmpleado = f.IdEmpleado
            LEFT JOIN DetalleFactura d ON d.IdFactura = f.IdFactura
            GROUP BY
                f.IdFactura, f.IdCliente, c.Nombre, f.IdEmpleado, e.Nombre,
                f.FechaRegistro, f.Estado, f.Descuento, f.Iva
            ORDER BY f.IdFactura
        """
        return self.acceso_datos.ejecutar_consulta(sql)

    def consultar_detalle(self, id_factura: int) -> List[dict]:
        sql = """
            SELECT d.IdDetalle, d.IdProducto, p.Nombre AS ProductoNombre, d.Cantidad, d.Precio
            FROM DetalleFactura d
            LEFT JOIN Productos p ON p.IdProducto = d.IdProducto
            WHERE d.IdFactura = ?
        """
        return self.acceso_datos.ejecutar_consulta(sql, [id_factura])

    def insertar(self, factura: Factura) -> int:
        sql_encabezado = (
            "INSERT INTO Facturas (IdCliente, IdEmpleado, FechaRegistro, Estado, Descuento, Iva) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        id_factura = self.acceso_datos.ejecutar_insert_devolviendo_id(
            sql_encabezado,
            [
                factura.cliente.id_cliente,
                factura.empleado.id_empleado,
                factura.fecha_registro,
                factura.estado,
                factura.descuento,
                factura.iva,
            ],
        )

        sql_detalle = (
            "INSERT INTO DetalleFactura (IdFactura, IdProducto, Cantidad, Precio) VALUES (?, ?, ?, ?)"
        )
        for detalle in factura.detalles:
            self.acceso_datos.ejecutar_comando(
                sql_detalle,
                [id_factura, detalle.producto.id_producto, detalle.cantidad, detalle.precio],
            )

        return id_factura

    def eliminar(self, id_factura: int) -> None:
        self.acceso_datos.ejecutar_comando(
            "DELETE FROM Facturas WHERE IdFactura = ?", [id_factura]
        )

    def actualizar(self, factura: Factura) -> None:
        sql_encabezado = (
            "UPDATE Facturas SET IdCliente = ?, IdEmpleado = ?, Estado = ?, "
            "Descuento = ?, Iva = ? WHERE IdFactura = ?"
        )
        self.acceso_datos.ejecutar_comando(
            sql_encabezado,
            [
                factura.cliente.id_cliente,
                factura.empleado.id_empleado,
                factura.estado,
                factura.descuento,
                factura.iva,
                factura.id_factura,
            ],
        )

        self.acceso_datos.ejecutar_comando(
            "DELETE FROM DetalleFactura WHERE IdFactura = ?", [factura.id_factura]
        )
        sql_detalle = (
            "INSERT INTO DetalleFactura (IdFactura, IdProducto, Cantidad, Precio) VALUES (?, ?, ?, ?)"
        )
        for detalle in factura.detalles:
            self.acceso_datos.ejecutar_comando(
                sql_detalle,
                [factura.id_factura, detalle.producto.id_producto, detalle.cantidad, detalle.precio],
            )
