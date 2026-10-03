"""Capa de Datos: acceso a la tabla Productos en SQL Server."""
from typing import List

from acceso_datos import AccesoDatos
from capa_entidades.producto import Producto


class ProductoDatos:
    def __init__(self):
        self.acceso_datos = AccesoDatos()

    def consultar_todos(self) -> List[dict]:
        return self.acceso_datos.ejecutar_consulta(
            "SELECT IdProducto, Nombre, Categoria, Precio, Stock FROM Productos"
        )

    def insertar(self, producto: Producto) -> None:
        sql = "INSERT INTO Productos (Nombre, Categoria, Precio, Stock) VALUES (?, ?, ?, ?)"
        self.acceso_datos.ejecutar_comando(
            sql, [producto.nombre, producto.categoria, producto.precio, producto.stock]
        )

    def actualizar(self, id_producto: int, producto: Producto) -> None:
        sql = (
            "UPDATE Productos SET Nombre = ?, Categoria = ?, Precio = ?, Stock = ? "
            "WHERE IdProducto = ?"
        )
        self.acceso_datos.ejecutar_comando(
            sql, [producto.nombre, producto.categoria, producto.precio, producto.stock, id_producto]
        )

    def eliminar(self, id_producto: int) -> None:
        self.acceso_datos.ejecutar_comando(
            "DELETE FROM Productos WHERE IdProducto = ?", [id_producto]
        )

    def ajustar_stock(self, id_producto: int, delta: int) -> None:
        """Suma 'delta' unidades al stock actual (pasa un número
        negativo para descontar). Se hace con una sola instrucción
        'Stock = Stock + ?' en vez de leer y luego escribir, para que
        el ajuste sea atómico a nivel de SQL Server. La usa
        FacturaNegocio para mantener el stock sincronizado con lo que
        se factura."""
        self.acceso_datos.ejecutar_comando(
            "UPDATE Productos SET Stock = Stock + ? WHERE IdProducto = ?",
            [delta, id_producto],
        )
