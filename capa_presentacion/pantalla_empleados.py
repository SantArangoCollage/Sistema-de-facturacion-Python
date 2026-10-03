"""
Capa de Presentación: CRUD de Empleados.

Esta pantalla NO contiene SQL ni conoce pyodbc: recolecta lo que
escribe el usuario y se lo entrega a EmpleadoNegocio (Capa de
Negocio), que valida las reglas del negocio y delega en EmpleadoDatos
(Capa de Datos) para guardar en SQL Server.
"""
import tkinter as tk

from acceso_datos import ErrorBaseDatos
from capa_negocio.empleado_negocio import EmpleadoNegocio
from capa_negocio.validaciones import ErrorValidacion
from dialogo_persona import DialogoPersona
from ui_common import FUENTE_TITULO, confirmar, crear_treeview, error, obtener_seleccion


class PantallaListaEmpleados(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white", padx=16, pady=16)
        self.negocio = EmpleadoNegocio()
        self.empleados_cargados = []  # dicts tal como vienen de la BD, mismo orden que la tabla

        tk.Label(self, text="Empleados", font=FUENTE_TITULO, bg="white").pack(
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
            self.empleados_cargados = self.negocio.listar()
        except ErrorBaseDatos as ex:
            error(str(ex))
            self.empleados_cargados = []

        self.tree.delete(*self.tree.get_children())
        for empleado in self.empleados_cargados:
            self.tree.insert(
                "",
                "end",
                values=(
                    empleado["Nombre"],
                    empleado["Documento"],
                    empleado["Direccion"],
                    empleado["Telefono"],
                    empleado["Email"],
                ),
            )

    def _nuevo(self):
        dlg = DialogoPersona(self, "Nuevo empleado")
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
        seleccionado = obtener_seleccion(self.tree, self.empleados_cargados)
        if seleccionado is None:
            return

        clase_temporal = type("EmpleadoTemp", (), {})()
        clase_temporal.nombre = seleccionado["Nombre"]
        clase_temporal.documento = seleccionado["Documento"]
        clase_temporal.direccion = seleccionado["Direccion"]
        clase_temporal.telefono = seleccionado["Telefono"]
        clase_temporal.email = seleccionado["Email"]

        dlg = DialogoPersona(self, "Editar empleado", persona=clase_temporal)
        datos = dlg.esperar()
        if datos is None:
            return

        try:
            self.negocio.editar(
                seleccionado["IdEmpleado"],
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
        seleccionado = obtener_seleccion(self.tree, self.empleados_cargados)
        if seleccionado is None:
            return
        if not confirmar("Confirmar", "¿Eliminar empleado?"):
            return

        try:
            self.negocio.eliminar(seleccionado["IdEmpleado"])
        except ErrorBaseDatos as ex:
            error(str(ex))
            return

        self._cargar_grilla()
