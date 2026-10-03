"""
Capa de Datos: acceso a la tabla Usuarios (seguridad) en SQL Server.
"""
from typing import List, Optional

from acceso_datos import AccesoDatos
from capa_entidades.usuario import Usuario


class UsuarioDatos:
    def __init__(self):
        self.acceso_datos = AccesoDatos()

    def consultar_todos(self) -> List[dict]:
        return self.acceso_datos.ejecutar_consulta(
            "SELECT IdUsuario, Nombre, Usuario, Password, Rol FROM Usuarios"
        )

    def consultar_por_credenciales(self, usuario: str, clave: str) -> Optional[dict]:
        filas = self.acceso_datos.ejecutar_consulta(
            "SELECT IdUsuario, Nombre, Usuario, Password, Rol "
            "FROM Usuarios WHERE Usuario = ? AND Password = ?",
            [usuario, clave],
        )
        return filas[0] if filas else None

    def existe_login(self, login: str, excluir_id: Optional[int] = None) -> bool:
        filas = self.acceso_datos.ejecutar_consulta(
            "SELECT IdUsuario FROM Usuarios WHERE Usuario = ?", [login]
        )
        return any(f["IdUsuario"] != excluir_id for f in filas)

    def insertar(self, usuario: Usuario) -> None:
        sql = "INSERT INTO Usuarios (Nombre, Usuario, Password, Rol) VALUES (?, ?, ?, ?)"
        self.acceso_datos.ejecutar_comando(
            sql, [usuario.nombre, usuario.login, usuario.clave, usuario.rol]
        )

    def actualizar(self, id_usuario: int, usuario: Usuario) -> None:
        sql = (
            "UPDATE Usuarios SET Nombre = ?, Usuario = ?, Password = ?, Rol = ? "
            "WHERE IdUsuario = ?"
        )
        self.acceso_datos.ejecutar_comando(
            sql, [usuario.nombre, usuario.login, usuario.clave, usuario.rol, id_usuario]
        )

    def eliminar(self, id_usuario: int) -> None:
        self.acceso_datos.ejecutar_comando(
            "DELETE FROM Usuarios WHERE IdUsuario = ?", [id_usuario]
        )
