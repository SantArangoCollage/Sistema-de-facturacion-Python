"""
Capa de Negocio: valida los datos de un Empleado y delega el acceso a
datos en EmpleadoDatos (Capa de Datos). La Capa de Presentación
(pantalla de Empleados) solo llama a esta clase, nunca a EmpleadoDatos
directamente ni ejecuta SQL.
"""
from typing import List

from capa_datos.empleado_datos import EmpleadoDatos
from capa_entidades.empleado import Empleado
from capa_negocio.manejo_errores import contexto_bd
from capa_negocio.validaciones import (
    validar_direccion,
    validar_documento,
    validar_email,
    validar_nombre,
    validar_telefono,
)


class EmpleadoNegocio:
    def __init__(self):
        self.datos = EmpleadoDatos()

    def listar(self) -> List[dict]:
        with contexto_bd("No se pudieron consultar los empleados"):
            return self.datos.consultar_todos()

    def _validar_y_construir(self, nombre, documento, telefono, direccion, email) -> Empleado:
        nombre = validar_nombre(nombre, campo="El nombre")
        documento = validar_documento(documento)
        telefono = validar_telefono(telefono)
        direccion = validar_direccion(direccion)
        email = validar_email(email)
        return Empleado(
            nombre=nombre, documento=documento, telefono=telefono, direccion=direccion, email=email
        )

    def crear(self, nombre: str, documento: str, telefono: str, direccion: str, email: str) -> None:
        empleado = self._validar_y_construir(nombre, documento, telefono, direccion, email)
        with contexto_bd("No se pudo guardar el empleado"):
            self.datos.insertar(empleado)

    def editar(
        self, id_empleado: int, nombre: str, documento: str, telefono: str, direccion: str, email: str
    ) -> None:
        empleado = self._validar_y_construir(nombre, documento, telefono, direccion, email)
        with contexto_bd("No se pudo actualizar el empleado"):
            self.datos.actualizar(id_empleado, empleado)

    def eliminar(self, id_empleado: int) -> None:
        with contexto_bd("No se pudo eliminar el empleado"):
            self.datos.eliminar(id_empleado)
