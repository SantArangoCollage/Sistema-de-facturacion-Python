import tkinter as tk
from tkinter import ttk

from acceso_datos import ErrorBaseDatos
from capa_negocio.cliente_negocio import ClienteNegocio
from capa_negocio.empleado_negocio import EmpleadoNegocio
from capa_negocio.factura_negocio import FacturaNegocio
from capa_negocio.producto_negocio import ProductoNegocio
from ui_common import FUENTE_TITULO, crear_treeview, error

TIPOS = ["Facturas", "Clientes", "Productos", "Empleados"]


class PantallaInformes(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white", padx=16, pady=16)
        self.cliente_negocio = ClienteNegocio()
        self.producto_negocio = ProductoNegocio()
        self.empleado_negocio = EmpleadoNegocio()
        self.factura_negocio = FacturaNegocio()

        tk.Label(self, text="Informes", font=FUENTE_TITULO, bg="white").pack(
            anchor="w", pady=(0, 10)
        )

        barra = tk.Frame(self, bg="white")
        barra.pack(anchor="w", pady=(0, 10))

        tk.Label(barra, text="Tipo", bg="white").pack(side="left", padx=(0, 6))
        self.cb_tipo = ttk.Combobox(barra, width=20, state="readonly", values=TIPOS)
        self.cb_tipo.current(0)
        self.cb_tipo.pack(side="left", padx=(0, 10))

        tk.Button(barra, text="Consultar", command=self._consultar).pack(side="left")

        self.frame_tabla = tk.Frame(self)
        self.frame_tabla.pack(fill="both", expand=True)
        self.tree = None

        self._consultar()

    def _mostrar_columnas(self, columnas):
        if self.tree is not None:
            self.tree.master.destroy()
        frame_tabla, self.tree = crear_treeview(self.frame_tabla, columnas)
        frame_tabla.pack(fill="both", expand=True)

    def _consultar(self):
        tipo = self.cb_tipo.get()

        if tipo == "Facturas":
            columnas = [
                ("numero", "N°", 50),
                ("cliente", "Cliente", 150),
                ("empleado", "Empleado", 150),
                ("fecha", "Fecha", 130),
                ("estado", "Estado", 90),
                ("total", "Total", 110),
            ]
            self._mostrar_columnas(columnas)
            try:
                filas = self.factura_negocio.listar()
            except ErrorBaseDatos as ex:
                error(str(ex))
                filas = []
            for f in filas:
                total = float(f["Subtotal"]) - float(f["Descuento"]) + float(f["Iva"])
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        f["IdFactura"],
                        f["ClienteNombre"] or "",
                        f["EmpleadoNombre"] or "",
                        f"{f['FechaRegistro']:%Y-%m-%d}",
                        f["Estado"],
                        f"{total:,.2f}",
                    ),
                )

        elif tipo == "Clientes":
            columnas = [
                ("nombre", "Nombre", 160),
                ("documento", "Documento", 110),
                ("direccion", "Dirección", 160),
                ("telefono", "Teléfono", 100),
                ("email", "Email", 180),
            ]
            self._mostrar_columnas(columnas)
            try:
                filas = self.cliente_negocio.listar()
            except ErrorBaseDatos as ex:
                error(str(ex))
                filas = []
            for c in filas:
                self.tree.insert(
                    "",
                    "end",
                    values=(c["Nombre"], c["Documento"], c["Direccion"], c["Telefono"], c["Email"]),
                )

        elif tipo == "Productos":
            columnas = [
                ("nombre", "Nombre", 160),
                ("categoria", "Categoría", 140),
                ("precio", "Precio", 100),
                ("stock", "Stock", 80),
            ]
            self._mostrar_columnas(columnas)
            try:
                filas = self.producto_negocio.listar()
            except ErrorBaseDatos as ex:
                error(str(ex))
                filas = []
            for p in filas:
                self.tree.insert(
                    "",
                    "end",
                    values=(p["Nombre"], p["Categoria"] or "", f"{float(p['Precio']):,.2f}", p["Stock"]),
                )

        elif tipo == "Empleados":
            columnas = [
                ("nombre", "Nombre", 160),
                ("documento", "Documento", 110),
                ("direccion", "Dirección", 160),
                ("telefono", "Teléfono", 100),
                ("email", "Email", 180),
            ]
            self._mostrar_columnas(columnas)
            try:
                filas = self.empleado_negocio.listar()
            except ErrorBaseDatos as ex:
                error(str(ex))
                filas = []
            for e in filas:
                self.tree.insert(
                    "",
                    "end",
                    values=(e["Nombre"], e["Documento"], e["Direccion"], e["Telefono"], e["Email"]),
                )
