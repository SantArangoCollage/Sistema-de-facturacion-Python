"""
Capa de Presentación: Seguridad · CRUD de Usuarios.

Igual que Empleados: esta pantalla no ejecuta SQL. Todo pasa por
UsuarioNegocio (Capa de Negocio) -> UsuarioDatos (Capa de Datos).
"""
import tkinter as tk
from tkinter import ttk

from acceso_datos import ErrorBaseDatos
from capa_negocio.usuario_negocio import ROLES_VALIDOS, UsuarioNegocio
from capa_negocio.validaciones import ErrorValidacion
from sesion import Sesion
from ui_common import (
    DialogoBase,
    FUENTE_NORMAL,
    FUENTE_TITULO,
    confirmar,
    crear_treeview,
    error,
    obtener_seleccion,
)


class DialogoUsuario(DialogoBase):
    def __init__(self, parent, negocio: UsuarioNegocio, usuario: dict = None):
        titulo = "Editar usuario" if usuario else "Nuevo usuario"
        super().__init__(parent, titulo)
        self.negocio = negocio
        self.usuario = usuario

        tk.Label(self, text="Nombre", font=FUENTE_NORMAL).grid(row=0, column=0, sticky="w", pady=4)
        self.txt_nombre = ttk.Entry(self, width=30)
        self.txt_nombre.grid(row=0, column=1, pady=4, padx=(10, 0))

        tk.Label(self, text="Login", font=FUENTE_NORMAL).grid(row=1, column=0, sticky="w", pady=4)
        self.txt_login = ttk.Entry(self, width=30)
        self.txt_login.grid(row=1, column=1, pady=4, padx=(10, 0))

        tk.Label(self, text="Clave", font=FUENTE_NORMAL).grid(row=2, column=0, sticky="w", pady=4)
        self.txt_clave = ttk.Entry(self, width=30, show="*")
        self.txt_clave.grid(row=2, column=1, pady=4, padx=(10, 0))

        tk.Label(self, text="Rol", font=FUENTE_NORMAL).grid(row=3, column=0, sticky="w", pady=4)
        self.cb_rol = ttk.Combobox(self, width=27, state="readonly", values=ROLES_VALIDOS)
        self.cb_rol.grid(row=3, column=1, pady=4, padx=(10, 0))

        if usuario is not None:
            self.txt_nombre.insert(0, usuario["Nombre"])
            self.txt_login.insert(0, usuario["Usuario"])
            self.txt_clave.insert(0, usuario["Password"])
            self.cb_rol.set(usuario["Rol"])
        else:
            self.cb_rol.set(ROLES_VALIDOS[0])

        botones = tk.Frame(self)
        botones.grid(row=4, column=0, columnspan=2, pady=(16, 0))
        tk.Button(botones, text="Guardar", width=12, command=self._guardar).pack(
            side="left", padx=4
        )
        tk.Button(
            botones, text="Salir", width=12, command=lambda: self.cerrar_con_resultado(None)
        ).pack(side="left", padx=4)

        self.txt_nombre.focus_set()

    def _guardar(self):
        nombre = self.txt_nombre.get().strip()
        login = self.txt_login.get().strip()
        clave = self.txt_clave.get()
        rol = self.cb_rol.get()

        id_usuario_actual = self.usuario["IdUsuario"] if self.usuario else None

        try:
            self.negocio.validar(nombre, login, clave, rol, id_usuario_actual=id_usuario_actual)
        except (ErrorValidacion, ErrorBaseDatos) as ex:
            error(str(ex))
            return

        self.cerrar_con_resultado({"nombre": nombre, "login": login, "clave": clave, "rol": rol})


class PantallaListaUsuarios(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white", padx=16, pady=16)
        self.negocio = UsuarioNegocio()
        self.usuarios_cargados = []

        tk.Label(self, text="Seguridad · Usuarios", font=FUENTE_TITULO, bg="white").pack(
            anchor="w", pady=(0, 10)
        )

        barra_botones = tk.Frame(self, bg="white")
        barra_botones.pack(anchor="w", pady=(0, 10))
        tk.Button(barra_botones, text="Nuevo", width=10, command=self._nuevo).pack(
            side="left", padx=(0, 6)
        )
        tk.Button(barra_botones, text="Editar", width=10, command=self._editar).pack(
            side="left", padx=6
        )
        tk.Button(barra_botones, text="Eliminar", width=10, command=self._eliminar).pack(
            side="left", padx=6
        )

        columnas = [
            ("nombre", "Nombre", 160),
            ("login", "Login", 120),
            ("rol", "Rol", 120),
        ]
        frame_tabla, self.tree = crear_treeview(self, columnas)
        frame_tabla.pack(fill="both", expand=True)

        self._cargar_grilla()

    def _cargar_grilla(self):
        try:
            self.usuarios_cargados = self.negocio.listar()
        except ErrorBaseDatos as ex:
            error(str(ex))
            self.usuarios_cargados = []

        self.tree.delete(*self.tree.get_children())
        for usuario in self.usuarios_cargados:
            self.tree.insert(
                "", "end", values=(usuario["Nombre"], usuario["Usuario"], usuario["Rol"])
            )

    def _nuevo(self):
        datos = DialogoUsuario(self, negocio=self.negocio).esperar()
        if datos is None:
            return

        try:
            self.negocio.crear(datos["nombre"], datos["login"], datos["clave"], datos["rol"])
        except (ErrorValidacion, ErrorBaseDatos) as ex:
            error(str(ex))
            return

        self._cargar_grilla()

    def _editar(self):
        seleccionado = obtener_seleccion(self.tree, self.usuarios_cargados)
        if seleccionado is None:
            return

        datos = DialogoUsuario(self, negocio=self.negocio, usuario=seleccionado).esperar()
        if datos is None:
            return

        try:
            self.negocio.editar(
                seleccionado["IdUsuario"], datos["nombre"], datos["login"], datos["clave"], datos["rol"]
            )
        except (ErrorValidacion, ErrorBaseDatos) as ex:
            error(str(ex))
            return

        self._cargar_grilla()

    def _eliminar(self):
        seleccionado = obtener_seleccion(self.tree, self.usuarios_cargados)
        if seleccionado is None:
            return

        if seleccionado["IdUsuario"] == Sesion.id_usuario:
            error("No puede eliminar el usuario con el que inició sesión")
            return

        if not confirmar("Confirmar", "¿Eliminar usuario?"):
            return

        try:
            self.negocio.eliminar(seleccionado["IdUsuario"])
        except ErrorBaseDatos as ex:
            error(str(ex))
            return

        self._cargar_grilla()
