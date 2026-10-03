"""
Capa de Presentación: CRUD de Productos.

Mismo patrón que Empleados/Clientes. El diálogo valida contra
ProductoNegocio ANTES de cerrarse (nombre, categoría, precio, stock),
así que un dato inválido se queda en pantalla para corregir en vez de
cerrar la ventana y perder lo ya escrito.
"""
import tkinter as tk
from tkinter import ttk

from acceso_datos import ErrorBaseDatos
from capa_negocio.producto_negocio import ProductoNegocio
from capa_negocio.validaciones import ErrorValidacion
from datos_sistema import DatosSistema
from ui_common import (
    DialogoBase,
    FUENTE_NORMAL,
    FUENTE_TITULO,
    confirmar,
    crear_treeview,
    error,
    obtener_seleccion,
)


class DialogoProducto(DialogoBase):
    def __init__(self, parent, negocio: ProductoNegocio, producto: dict = None):
        titulo = "Editar producto" if producto else "Nuevo producto"
        super().__init__(parent, titulo)
        self.negocio = negocio
        self.producto = producto

        tk.Label(self, text="Nombre", font=FUENTE_NORMAL).grid(row=0, column=0, sticky="w", pady=4)
        self.txt_nombre = ttk.Entry(self, width=30)
        self.txt_nombre.grid(row=0, column=1, pady=4, padx=(10, 0))

        tk.Label(self, text="Categoría", font=FUENTE_NORMAL).grid(
            row=1, column=0, sticky="w", pady=4
        )
        self.cb_categoria = ttk.Combobox(
            self, width=27, state="readonly", values=[str(c) for c in DatosSistema.categorias]
        )
        self.cb_categoria.grid(row=1, column=1, pady=4, padx=(10, 0))

        tk.Label(self, text="Precio", font=FUENTE_NORMAL).grid(row=2, column=0, sticky="w", pady=4)
        self.txt_precio = ttk.Entry(self, width=30)
        self.txt_precio.grid(row=2, column=1, pady=4, padx=(10, 0))

        tk.Label(self, text="Stock", font=FUENTE_NORMAL).grid(row=3, column=0, sticky="w", pady=4)
        self.txt_stock = ttk.Entry(self, width=30)
        self.txt_stock.grid(row=3, column=1, pady=4, padx=(10, 0))

        if producto is not None:
            self.txt_nombre.insert(0, producto["Nombre"])
            if producto["Categoria"]:
                self.cb_categoria.set(producto["Categoria"])
            self.txt_precio.insert(0, str(producto["Precio"]))
            self.txt_stock.insert(0, str(producto["Stock"]))

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
        categoria = self.cb_categoria.get()
        precio = self.txt_precio.get().strip()
        stock = self.txt_stock.get().strip()

        try:
            # Solo valida (no guarda nada todavía): si algo está mal, se
            # queda en esta ventana para corregir, en vez de cerrarla.
            self.negocio.validar(nombre, categoria, precio, stock)
        except ErrorValidacion as ex:
            error(str(ex))
            return

        self.cerrar_con_resultado(
            {"nombre": nombre, "categoria": categoria, "precio": precio, "stock": stock}
        )


class PantallaListaProductos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white", padx=16, pady=16)
        self.negocio = ProductoNegocio()
        self.productos_cargados = []

        tk.Label(self, text="Productos", font=FUENTE_TITULO, bg="white").pack(
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
            ("categoria", "Categoría", 140),
            ("precio", "Precio", 100),
            ("stock", "Stock", 80),
        ]
        frame_tabla, self.tree = crear_treeview(self, columnas)
        frame_tabla.pack(fill="both", expand=True)

        self._cargar_grilla()

    def _cargar_grilla(self):
        try:
            self.productos_cargados = self.negocio.listar()
        except ErrorBaseDatos as ex:
            error(str(ex))
            self.productos_cargados = []

        self.tree.delete(*self.tree.get_children())
        for producto in self.productos_cargados:
            self.tree.insert(
                "",
                "end",
                values=(
                    producto["Nombre"],
                    producto["Categoria"] or "",
                    f"{float(producto['Precio']):,.2f}",
                    producto["Stock"],
                ),
            )

    def _nuevo(self):
        datos = DialogoProducto(self, negocio=self.negocio).esperar()
        if datos is None:
            return

        try:
            self.negocio.crear(datos["nombre"], datos["categoria"], datos["precio"], datos["stock"])
        except (ErrorValidacion, ErrorBaseDatos) as ex:
            error(str(ex))
            return

        self._cargar_grilla()

    def _editar(self):
        seleccionado = obtener_seleccion(self.tree, self.productos_cargados)
        if seleccionado is None:
            return

        datos = DialogoProducto(self, negocio=self.negocio, producto=seleccionado).esperar()
        if datos is None:
            return

        try:
            self.negocio.editar(
                seleccionado["IdProducto"], datos["nombre"], datos["categoria"], datos["precio"], datos["stock"]
            )
        except (ErrorValidacion, ErrorBaseDatos) as ex:
            error(str(ex))
            return

        self._cargar_grilla()

    def _eliminar(self):
        seleccionado = obtener_seleccion(self.tree, self.productos_cargados)
        if seleccionado is None:
            return
        if not confirmar("Confirmar", "¿Eliminar producto?"):
            return

        try:
            self.negocio.eliminar(seleccionado["IdProducto"])
        except ErrorBaseDatos as ex:
            error(str(ex))
            return

        self._cargar_grilla()
