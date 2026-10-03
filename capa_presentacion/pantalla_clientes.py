"""
Capa de Presentación: CRUD de Clientes.

Mismo patrón que Empleados: esta pantalla no ejecuta SQL ni conoce
pyodbc. Todo pasa por ClienteNegocio (Capa de Negocio) -> ClienteDatos
(Capa de Datos). El diálogo (dialogo_persona.py) ya valida los campos
antes de cerrarse, así que aquí solo queda atrapar errores de base de
datos (ej. que el servidor no responda) al guardar/eliminar.
"""
import tkinter as tk

from acceso_datos import ErrorBaseDatos
from capa_negocio.cliente_negocio import ClienteNegocio
from capa_negocio.validaciones import ErrorValidacion
from dialogo_persona import DialogoPersona
from ui_common import FUENTE_TITULO, confirmar, crear_treeview, error, obtener_seleccion


class PantallaListaClientes(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white", padx=16, pady=16)
        self.negocio = ClienteNegocio()
        self.clientes_cargados = []  # dicts tal como vienen de la BD, mismo orden que la tabla

        tk.Label(self, text="Clientes", font=FUENTE_TITULO, bg="white").pack(
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
            ("documento", "Documento", 110),
            ("direccion", "Dirección", 160),
            ("telefono", "Teléfono", 100),
            ("email", "Email", 180),
        ]
        frame_tabla, self.tree = crear_treeview(self, columnas)
        frame_tabla.pack(fill="both", expand=True)

        self._cargar_grilla()

    def _cargar_grilla(self):
        try:
            self.clientes_cargados = self.negocio.listar()
        except ErrorBaseDatos as ex:
            error(str(ex))
            self.clientes_cargados = []

        self.tree.delete(*self.tree.get_children())
        for cliente in self.clientes_cargados:
            self.tree.insert(
                "",
                "end",
                values=(
                    cliente["Nombre"],
                    cliente["Documento"],
                    cliente["Direccion"],
                    cliente["Telefono"],
                    cliente["Email"],
                ),
            )

    def _nuevo(self):
        dlg = DialogoPersona(self, "Nuevo cliente")
        datos = dlg.esperar()
        if datos is None:
            return

        try:
            self.negocio.crear(
                datos["nombre"], datos["documento"], datos["telefono"], datos["direccion"], datos["email"]
            )
        except (ErrorValidacion, ErrorBaseDatos) as ex:
            error(str(ex))
            return

        self._cargar_grilla()

    def _editar(self):
        seleccionado = obtener_seleccion(self.tree, self.clientes_cargados)
        if seleccionado is None:
            return

        clase_temporal = type("ClienteTemp", (), {})()
        clase_temporal.nombre = seleccionado["Nombre"]
        clase_temporal.documento = seleccionado["Documento"]
        clase_temporal.direccion = seleccionado["Direccion"]
        clase_temporal.telefono = seleccionado["Telefono"]
        clase_temporal.email = seleccionado["Email"]

        dlg = DialogoPersona(self, "Editar cliente", persona=clase_temporal)
        datos = dlg.esperar()
        if datos is None:
            return

        try:
            self.negocio.editar(
                seleccionado["IdCliente"],
                datos["nombre"],
                datos["documento"],
                datos["telefono"],
                datos["direccion"],
                datos["email"],
            )
        except (ErrorValidacion, ErrorBaseDatos) as ex:
            error(str(ex))
            return

        self._cargar_grilla()

    def _eliminar(self):
        seleccionado = obtener_seleccion(self.tree, self.clientes_cargados)
        if seleccionado is None:
            return
        if not confirmar("Confirmar", "¿Eliminar cliente?"):
            return

        try:
            self.negocio.eliminar(seleccionado["IdCliente"])
        except ErrorBaseDatos as ex:
            error(str(ex))
            return

        self._cargar_grilla()
