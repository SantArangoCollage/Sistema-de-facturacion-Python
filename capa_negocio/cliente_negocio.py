"""
Capa de Negocio: valida los datos de un Cliente y delega el acceso a
datos en ClienteDatos (Capa de Datos). Mismo patrón que EmpleadoNegocio.
"""
from typing import List

from capa_datos.cliente_datos import ClienteDatos
from capa_entidades.cliente import Cliente
from capa_negocio.manejo_errores import contexto_bd
from capa_negocio.validaciones import (
    validar_direccion,
    validar_documento,
    validar_email,
    validar_nombre,
    validar_telefono,
)


class ClienteNegocio:
    def __init__(self):
        self.datos = ClienteDatos()

    def listar(self) -> List[dict]:
        with contexto_bd("No se pudieron consultar los clientes"):
            return self.datos.consultar_todos()

    def validar(self, nombre, documento, telefono, direccion, email) -> Cliente:
        nombre = validar_nombre(nombre, campo="El nombre")
        documento = validar_documento(documento)
        telefono = validar_telefono(telefono)
        direccion = validar_direccion(direccion)
        email = validar_email(email)
        return Cliente(
            nombre=nombre, documento=documento, telefono=telefono, direccion=direccion, email=email
        )

    def crear(self, nombre: str, documento: str, telefono: str, direccion: str, email: str) -> None:
        cliente = self.validar(nombre, documento, telefono, direccion, email)
        with contexto_bd("No se pudo guardar el cliente"):
            self.datos.insertar(cliente)

    def editar(
        self, id_cliente: int, nombre: str, documento: str, telefono: str, direccion: str, email: str
    ) -> None:
        cliente = self.validar(nombre, documento, telefono, direccion, email)
        with contexto_bd("No se pudo actualizar el cliente"):
            self.datos.actualizar(id_cliente, cliente)

    def eliminar(self, id_cliente: int) -> None:
        with contexto_bd("No se pudo eliminar el cliente"):
            self.datos.eliminar(id_cliente)
