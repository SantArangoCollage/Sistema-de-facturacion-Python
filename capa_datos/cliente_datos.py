"""Capa de Datos: acceso a la tabla Clientes en SQL Server."""
from typing import List

from acceso_datos import AccesoDatos
from capa_entidades.cliente import Cliente


class ClienteDatos:
    def __init__(self):
        self.acceso_datos = AccesoDatos()

    def consultar_todos(self) -> List[dict]:
        return self.acceso_datos.ejecutar_consulta(
            "SELECT IdCliente, Nombre, Documento, Telefono, Direccion, Email FROM Clientes"
        )

    def insertar(self, cliente: Cliente) -> None:
        sql = (
            "INSERT INTO Clientes (Nombre, Documento, Telefono, Direccion, Email) "
            "VALUES (?, ?, ?, ?, ?)"
        )
        self.acceso_datos.ejecutar_comando(
            sql,
            [cliente.nombre, cliente.documento, cliente.telefono, cliente.direccion, cliente.email],
        )

    def actualizar(self, id_cliente: int, cliente: Cliente) -> None:
        sql = (
            "UPDATE Clientes SET Nombre = ?, Documento = ?, Telefono = ?, "
            "Direccion = ?, Email = ? WHERE IdCliente = ?"
        )
        self.acceso_datos.ejecutar_comando(
            sql,
            [
                cliente.nombre,
                cliente.documento,
                cliente.telefono,
                cliente.direccion,
                cliente.email,
                id_cliente,
            ],
        )

    def eliminar(self, id_cliente: int) -> None:
        self.acceso_datos.ejecutar_comando("DELETE FROM Clientes WHERE IdCliente = ?", [id_cliente])
