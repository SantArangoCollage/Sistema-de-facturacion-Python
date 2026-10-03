"""
Capa de Datos: acceso a la tabla Empleados en SQL Server.

Esta capa NO valida reglas de negocio (eso es trabajo de la Capa de
Negocio) — solo sabe ejecutar las consultas SQL necesarias, usando la
infraestructura genérica de acceso_datos.py.
"""
from typing import List

from acceso_datos import AccesoDatos
from capa_entidades.empleado import Empleado


class EmpleadoDatos:
    def __init__(self):
        self.acceso_datos = AccesoDatos()

    def consultar_todos(self) -> List[dict]:
        return self.acceso_datos.ejecutar_consulta(
            "SELECT IdEmpleado, Nombre, Documento, Telefono, Direccion, Email FROM Empleados"
        )

    def insertar(self, empleado: Empleado) -> None:
        sql = (
            "INSERT INTO Empleados (Nombre, Documento, Telefono, Direccion, Email) "
            "VALUES (?, ?, ?, ?, ?)"
        )
        self.acceso_datos.ejecutar_comando(
            sql,
            [
                empleado.nombre,
                empleado.documento,
                empleado.telefono,
                empleado.direccion,
                empleado.email,
            ],
        )

    def actualizar(self, id_empleado: int, empleado: Empleado) -> None:
        sql = (
            "UPDATE Empleados SET Nombre = ?, Documento = ?, Telefono = ?, "
            "Direccion = ?, Email = ? WHERE IdEmpleado = ?"
        )
        self.acceso_datos.ejecutar_comando(
            sql,
            [
                empleado.nombre,
                empleado.documento,
                empleado.telefono,
                empleado.direccion,
                empleado.email,
                id_empleado,
            ],
        )

    def eliminar(self, id_empleado: int) -> None:
        self.acceso_datos.ejecutar_comando(
            "DELETE FROM Empleados WHERE IdEmpleado = ?", [id_empleado]
        )
