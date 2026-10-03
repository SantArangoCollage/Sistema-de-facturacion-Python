"""
Capa de Negocio: valida los datos de Usuario y las credenciales de
login, delegando el acceso a datos en UsuarioDatos (Capa de Datos).
"""
from typing import List, Optional

from capa_datos.usuario_datos import UsuarioDatos
from capa_entidades.usuario import Usuario
from capa_negocio.manejo_errores import contexto_bd
from capa_negocio.validaciones import ErrorValidacion, validar_nombre

ROLES_VALIDOS = ["Administrador", "Cajero"]


class UsuarioNegocio:
    def __init__(self):
        self.datos = UsuarioDatos()

    def listar(self) -> List[dict]:
        with contexto_bd("No se pudieron consultar los usuarios"):
            return self.datos.consultar_todos()

    def validar_credenciales(self, usuario: str, clave: str) -> Optional[dict]:
        """Regla de negocio del login: devuelve la fila del usuario si
        las credenciales son correctas, o None si no lo son."""
        usuario = (usuario or "").strip()
        if not usuario or not clave:
            return None
        with contexto_bd("No se pudo validar el inicio de sesión"):
            return self.datos.consultar_por_credenciales(usuario, clave)

    def validar(self, nombre, login, clave, rol, id_usuario_actual=None) -> Usuario:
        """Valida las reglas de negocio de un Usuario, sin guardar nada.
        Se usa tanto aquí (antes de insertar/actualizar) como desde el
        diálogo de la Capa de Presentación, para rechazar datos inválidos
        antes de cerrar la ventana."""
        nombre = validar_nombre(nombre, campo="El nombre")

        login = (login or "").strip()
        if not login:
            raise ErrorValidacion("El login es obligatorio")
        if len(login) < 4:
            raise ErrorValidacion("El login debe tener al menos 4 caracteres")

        if not clave:
            raise ErrorValidacion("La clave es obligatoria")
        if len(clave) < 4:
            raise ErrorValidacion("La clave debe tener al menos 4 caracteres")

        if rol not in ROLES_VALIDOS:
            raise ErrorValidacion("Seleccione un rol válido")

        with contexto_bd("No se pudo verificar el login"):
            login_duplicado = self.datos.existe_login(login, excluir_id=id_usuario_actual)
        if login_duplicado:
            raise ErrorValidacion("Ese login ya está en uso por otro usuario")

        return Usuario(nombre=nombre, login=login, clave=clave, rol=rol)

    def crear(self, nombre: str, login: str, clave: str, rol: str) -> None:
        usuario = self.validar(nombre, login, clave, rol)
        with contexto_bd("No se pudo guardar el usuario"):
            self.datos.insertar(usuario)

    def editar(self, id_usuario: int, nombre: str, login: str, clave: str, rol: str) -> None:
        usuario = self.validar(nombre, login, clave, rol, id_usuario_actual=id_usuario)
        with contexto_bd("No se pudo actualizar el usuario"):
            self.datos.actualizar(id_usuario, usuario)

    def eliminar(self, id_usuario: int) -> None:
        with contexto_bd("No se pudo eliminar el usuario"):
            self.datos.eliminar(id_usuario)
