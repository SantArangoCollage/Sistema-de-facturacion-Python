"""
Capa de Presentación: Facturación.

Mismo patrón que Clientes/Productos/Empleados: esta pantalla no
ejecuta SQL. Todo pasa por FacturaNegocio (Capa de Negocio), que a su
vez reutiliza ClienteNegocio/ProductoNegocio/EmpleadoNegocio para los
combobox, y FacturaDatos (Capa de Datos) para guardar/consultar.
"""
import tkinter as tk
from tkinter import simpledialog, ttk

from acceso_datos import ErrorBaseDatos
from capa_entidades.detalle_factura import DetalleFactura
from capa_entidades.producto import Producto
from capa_negocio.factura_negocio import ESTADOS_VALIDOS, PORCENTAJE_IVA, FacturaNegocio
from capa_negocio.validaciones import ErrorValidacion, validar_cantidad
from ui_common import (
    DialogoBase,
    FUENTE_NORMAL,
    FUENTE_TITULO,
    confirmar,
    crear_treeview,
    error,
    info,
    obtener_seleccion,
)


class DialogoNuevaFactura(DialogoBase):
    """Formulario para crear o editar una factura, con su detalle de productos."""
    def __init__(
        self,
        parent,
        negocio: FacturaNegocio,
        factura_existente: dict = None,
        detalles_existentes: list = None,
    ):
        self.id_factura = factura_existente["IdFactura"] if factura_existente else None
        titulo = f"Editar factura N° {self.id_factura}" if self.id_factura else "Nueva factura"
        super().__init__(parent, titulo)
        self.negocio = negocio
        self.detalles_actuales = []  # list[DetalleFactura]

        try:
            self.clientes = negocio.obtener_clientes()
            self.productos = negocio.obtener_productos()
            self.empleados = negocio.obtener_empleados()
        except ErrorBaseDatos as ex:
            error(str(ex))
            self.clientes, self.productos, self.empleados = [], [], []

        # ---- Encabezado: cliente / empleado / estado ----
        encabezado = tk.Frame(self)
        encabezado.grid(row=0, column=0, sticky="w")

        tk.Label(encabezado, text="Cliente", font=FUENTE_NORMAL).grid(row=0, column=0, sticky="w")
        self.cb_cliente = ttk.Combobox(
            encabezado, width=25, state="readonly", values=[str(c) for c in self.clientes]
        )
        self.cb_cliente.grid(row=0, column=1, padx=(6, 20))

        tk.Label(encabezado, text="Empleado", font=FUENTE_NORMAL).grid(row=0, column=2, sticky="w")
        self.cb_empleado = ttk.Combobox(
            encabezado, width=25, state="readonly", values=[str(e) for e in self.empleados]
        )
        self.cb_empleado.grid(row=0, column=3, padx=(6, 20))

        tk.Label(encabezado, text="Estado", font=FUENTE_NORMAL).grid(row=0, column=4, sticky="w")
        self.cb_estado = ttk.Combobox(encabezado, width=12, state="readonly", values=ESTADOS_VALIDOS)
        self.cb_estado.current(0)
        self.cb_estado.grid(row=0, column=5, padx=(6, 0))

        # ---- Agregar producto al detalle ----
        panel_agregar = tk.Frame(self)
        panel_agregar.grid(row=1, column=0, sticky="w", pady=(16, 6))

        tk.Label(panel_agregar, text="Producto", font=FUENTE_NORMAL).grid(row=0, column=0, sticky="w")
        self.cb_producto = ttk.Combobox(
            panel_agregar,
            width=30,
            state="readonly",
            values=[f"{p.nombre} (stock: {p.stock})" for p in self.productos],
        )
        self.cb_producto.grid(row=0, column=1, padx=(6, 20))

        tk.Label(panel_agregar, text="Cantidad", font=FUENTE_NORMAL).grid(row=0, column=2, sticky="w")
        self.spin_cantidad = tk.Spinbox(panel_agregar, from_=1, to=999999, width=8)
        self.spin_cantidad.grid(row=0, column=3, padx=(6, 20))

        tk.Button(panel_agregar, text="Agregar", command=self._agregar_detalle).grid(
            row=0, column=4
        )

        # ---- Tabla de detalle (editable: se puede quitar o cambiar la
        # cantidad de una línea ya agregada, antes de guardar) ----
        columnas = [
            ("producto", "Producto", 180),
            ("cantidad", "Cantidad", 80),
            ("precio", "Precio", 100),
            ("subtotal", "Subtotal", 100),
        ]
        frame_tabla, self.tree_detalle = crear_treeview(self, columnas)
        frame_tabla.grid(row=2, column=0, sticky="nsew", pady=(0, 6))
        self.grid_rowconfigure(2, weight=1)
        self.tree_detalle.bind("<Double-1>", lambda e: self._editar_cantidad_detalle())

        acciones_detalle = tk.Frame(self)
        acciones_detalle.grid(row=3, column=0, sticky="w", pady=(0, 10))
        tk.Button(
            acciones_detalle,
            text="Editar cantidad",
            width=14,
            command=self._editar_cantidad_detalle,
        ).pack(side="left", padx=(0, 6))
        tk.Button(
            acciones_detalle,
            text="Quitar línea",
            width=14,
            command=self._quitar_detalle,
        ).pack(side="left")

        # ---- Totales ----
        panel_totales = tk.Frame(self)
        panel_totales.grid(row=4, column=0, sticky="e")

        tk.Label(panel_totales, text="Descuento", font=FUENTE_NORMAL).grid(row=0, column=0, sticky="e")
        self.txt_descuento = ttk.Entry(panel_totales, width=12)
        self.txt_descuento.insert(0, "0")
        self.txt_descuento.grid(row=0, column=1, padx=(6, 20))
        self.txt_descuento.bind("<KeyRelease>", lambda e: self._calcular_totales())

        tk.Label(panel_totales, text="IVA (19%)", font=FUENTE_NORMAL).grid(row=0, column=2, sticky="e")
        self.lbl_iva = tk.Label(panel_totales, text="0.00", font=FUENTE_NORMAL, width=12)
        self.lbl_iva.grid(row=0, column=3, padx=(6, 20))

        tk.Label(panel_totales, text="Total", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=4, sticky="e"
        )
        self.lbl_total = tk.Label(panel_totales, text="0.00", font=("Segoe UI", 11, "bold"), width=14)
        self.lbl_total.grid(row=0, column=5, padx=(6, 0))

        # ---- Botones finales ----
        botones = tk.Frame(self)
        botones.grid(row=5, column=0, pady=(16, 0))
        tk.Button(botones, text="Guardar factura", width=16, command=self._guardar).pack(
            side="left", padx=4
        )
        tk.Button(
            botones, text="Salir", width=12, command=lambda: self.cerrar_con_resultado(None)
        ).pack(side="left", padx=4)

        # ---- Modo edición: precargar cliente/empleado/estado/descuento
        # y las líneas ya guardadas de la factura ----
        if factura_existente is not None:
            self._precargar(factura_existente, detalles_existentes or [])
        else:
            self._calcular_totales()

    def _precargar(self, factura_existente: dict, detalles_existentes: list):
        indice_cliente = next(
            (i for i, c in enumerate(self.clientes) if c.id_cliente == factura_existente["IdCliente"]),
            -1,
        )
        if indice_cliente >= 0:
            self.cb_cliente.current(indice_cliente)

        indice_empleado = next(
            (i for i, e in enumerate(self.empleados) if e.id_empleado == factura_existente["IdEmpleado"]),
            -1,
        )
        if indice_empleado >= 0:
            self.cb_empleado.current(indice_empleado)

        if factura_existente["Estado"] in ESTADOS_VALIDOS:
            self.cb_estado.set(factura_existente["Estado"])

        self.txt_descuento.delete(0, "end")
        self.txt_descuento.insert(0, str(float(factura_existente["Descuento"])))

        for fila in detalles_existentes:
            producto = next(
                (p for p in self.productos if p.id_producto == fila["IdProducto"]), None
            )
            if producto is None:
                # El producto pudo haber sido eliminado desde que se
                # creó la factura; se arma uno "de respaldo" solo con
                # el nombre guardado, para no perder la línea.
                producto = Producto(
                    nombre=fila["ProductoNombre"] or "(producto eliminado)",
                    categoria="",
                    precio=float(fila["Precio"]),
                    stock=0,
                    id_producto=fila["IdProducto"],
                )
            else:
                # El stock en BD ya tiene restada esta cantidad (se
                # descontó cuando se guardó la factura la primera
                # vez). Para que las validaciones de esta sesión de
                # edición sean correctas, se "devuelve" en memoria —
                # son unidades que, mientras se edita, siguen siendo
                # de esta misma factura y se pueden reasignar
                # libremente entre sus líneas.
                producto.stock += fila["Cantidad"]

            self.detalles_actuales.append(
                DetalleFactura(
                    producto=producto,
                    cantidad=fila["Cantidad"],
                    precio=float(fila["Precio"]),
                )
            )

        # El combobox de productos ya se armó con el stock "crudo" de
        # BD; como algunos productos se ajustaron arriba, se vuelve a
        # armar su lista de textos para que muestre el stock correcto.
        self.cb_producto.configure(
            values=[f"{p.nombre} (stock: {p.stock})" for p in self.productos]
        )

        self._refrescar_tabla_detalle()

    def _refrescar_tabla_detalle(self):
        self.tree_detalle.delete(*self.tree_detalle.get_children())
        for detalle in self.detalles_actuales:
            self.tree_detalle.insert(
                "",
                "end",
                values=(
                    detalle.producto.nombre,
                    detalle.cantidad,
                    f"{detalle.precio:,.2f}",
                    f"{detalle.subtotal:,.2f}",
                ),
            )
        self._calcular_totales()

    def _cantidad_ya_reservada(self, id_producto, excluir_indice=None):
        """Cuántas unidades de ese producto ya están en OTRAS líneas
        del detalle que se está armando (para que la validación de
        stock sume todas las líneas del mismo producto, no solo la que
        se está agregando o editando en este momento)."""
        return sum(
            d.cantidad
            for i, d in enumerate(self.detalles_actuales)
            if d.producto.id_producto == id_producto and i != excluir_indice
        )

    def _agregar_detalle(self):
        indice_producto = self.cb_producto.current()
        if indice_producto < 0:
            error("Seleccione un producto")
            return

        producto = self.productos[indice_producto]
        ya_reservada = self._cantidad_ya_reservada(producto.id_producto)
        try:
            detalle = self.negocio.crear_detalle(producto, self.spin_cantidad.get(), ya_reservada)
        except ErrorValidacion as ex:
            error(str(ex))
            return

        self.detalles_actuales.append(detalle)
        self._refrescar_tabla_detalle()

    def _indice_seleccionado_detalle(self):
        seleccion = self.tree_detalle.selection()
        if not seleccion:
            error("Seleccione una línea del detalle")
            return None
        return self.tree_detalle.index(seleccion[0])

    def _quitar_detalle(self):
        indice = self._indice_seleccionado_detalle()
        if indice is None:
            return
        del self.detalles_actuales[indice]
        self._refrescar_tabla_detalle()

    def _editar_cantidad_detalle(self):
        indice = self._indice_seleccionado_detalle()
        if indice is None:
            return

        detalle = self.detalles_actuales[indice]
        nueva_cantidad = simpledialog.askinteger(
            "Editar cantidad",
            f"Nueva cantidad para '{detalle.producto.nombre}':",
            initialvalue=detalle.cantidad,
            minvalue=1,
            parent=self,
        )
        if nueva_cantidad is None:
            return

        ya_reservada = self._cantidad_ya_reservada(detalle.producto.id_producto, excluir_indice=indice)
        try:
            nueva_cantidad = validar_cantidad(nueva_cantidad, campo="La cantidad")
            self.negocio.validar_stock_disponible(detalle.producto, nueva_cantidad, ya_reservada)
        except ErrorValidacion as ex:
            error(str(ex))
            return

        detalle.cantidad = nueva_cantidad
        self._refrescar_tabla_detalle()

    def _calcular_totales(self):
        """Solo actualiza las etiquetas visuales; la validación real del
        descuento ocurre en FacturaNegocio.guardar() al confirmar."""
        subtotal = sum(d.subtotal for d in self.detalles_actuales)
        iva = subtotal * PORCENTAJE_IVA
        try:
            descuento = float(self.txt_descuento.get() or 0)
        except ValueError:
            descuento = 0.0

        self.lbl_iva.config(text=f"{iva:,.2f}")
        self.lbl_total.config(text=f"{subtotal + iva - descuento:,.2f}")

    def _guardar(self):
        indice_cliente = self.cb_cliente.current()
        cliente = self.clientes[indice_cliente] if indice_cliente >= 0 else None

        indice_empleado = self.cb_empleado.current()
        empleado = self.empleados[indice_empleado] if indice_empleado >= 0 else None

        estado = self.cb_estado.get()
        descuento = self.txt_descuento.get()

        try:
            if self.id_factura is None:
                self.negocio.guardar(cliente, empleado, estado, descuento, self.detalles_actuales)
            else:
                self.negocio.editar(
                    self.id_factura, cliente, empleado, estado, descuento, self.detalles_actuales
                )
        except (ErrorValidacion, ErrorBaseDatos) as ex:
            error(str(ex))
            return

        info("Factura actualizada correctamente" if self.id_factura else "Factura guardada correctamente")
        self.cerrar_con_resultado(True)


class DialogoVerFactura(DialogoBase):
    """Vista de solo lectura de una factura ya guardada."""

    def __init__(self, parent, negocio: FacturaNegocio, factura: dict):
        super().__init__(parent, f"Factura N° {factura['IdFactura']}")

        subtotal = float(factura["Subtotal"])
        descuento = float(factura["Descuento"])
        iva = float(factura["Iva"])
        total = subtotal - descuento + iva

        tk.Label(
            self,
            text=(
                f"Cliente: {factura['ClienteNombre'] or ''}\n"
                f"Empleado: {factura['EmpleadoNombre'] or ''}\n"
                f"Fecha: {factura['FechaRegistro']:%Y-%m-%d %H:%M}\n"
                f"Estado: {factura['Estado']}"
            ),
            font=FUENTE_NORMAL,
            justify="left",
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        columnas = [
            ("producto", "Producto", 180),
            ("cantidad", "Cantidad", 80),
            ("precio", "Precio", 100),
            ("subtotal", "Subtotal", 100),
        ]
        frame_tabla, tree = crear_treeview(self, columnas)
        frame_tabla.grid(row=1, column=0, sticky="nsew")

        try:
            detalles = negocio.listar_detalle(factura["IdFactura"])
        except ErrorBaseDatos as ex:
            error(str(ex))
            detalles = []

        for det in detalles:
            precio = float(det["Precio"])
            cantidad = det["Cantidad"]
            tree.insert(
                "",
                "end",
                values=(
                    det["ProductoNombre"] or "",
                    cantidad,
                    f"{precio:,.2f}",
                    f"{cantidad * precio:,.2f}",
                ),
            )

        tk.Label(
            self,
            text=f"Descuento: {descuento:,.2f}    IVA: {iva:,.2f}    Total: {total:,.2f}",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=2, column=0, sticky="e", pady=(10, 10))

        tk.Button(self, text="Cerrar", command=lambda: self.cerrar_con_resultado(None)).grid(
            row=3, column=0
        )


class PantallaListaFacturas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white", padx=16, pady=16)
        self.negocio = FacturaNegocio()
        self.facturas_cargadas = []

        tk.Label(self, text="Facturas", font=FUENTE_TITULO, bg="white").pack(
            anchor="w", pady=(0, 10)
        )

        barra_botones = tk.Frame(self, bg="white")
        barra_botones.pack(anchor="w", pady=(0, 10))
        tk.Button(barra_botones, text="Nueva", width=10, command=self._nueva).pack(
            side="left", padx=(0, 6)
        )
        tk.Button(barra_botones, text="Ver", width=10, command=self._ver).pack(
            side="left", padx=6
        )
        tk.Button(barra_botones, text="Editar", width=10, command=self._editar).pack(
            side="left", padx=6
        )
        tk.Button(barra_botones, text="Eliminar", width=10, command=self._eliminar).pack(
            side="left", padx=6
        )

        columnas = [
            ("numero", "N°", 50),
            ("cliente", "Cliente", 150),
            ("empleado", "Empleado", 150),
            ("fecha", "Fecha", 130),
            ("estado", "Estado", 90),
            ("total", "Total", 110),
        ]
        frame_tabla, self.tree = crear_treeview(self, columnas)
        frame_tabla.pack(fill="both", expand=True)

        self._cargar_grilla()

    def _cargar_grilla(self):
        try:
            self.facturas_cargadas = self.negocio.listar()
        except ErrorBaseDatos as ex:
            error(str(ex))
            self.facturas_cargadas = []

        self.tree.delete(*self.tree.get_children())
        for factura in self.facturas_cargadas:
            total = float(factura["Subtotal"]) - float(factura["Descuento"]) + float(factura["Iva"])
            self.tree.insert(
                "",
                "end",
                values=(
                    factura["IdFactura"],
                    factura["ClienteNombre"] or "",
                    factura["EmpleadoNombre"] or "",
                    f"{factura['FechaRegistro']:%Y-%m-%d}",
                    factura["Estado"],
                    f"{total:,.2f}",
                ),
            )

    def _nueva(self):
        resultado = DialogoNuevaFactura(self, negocio=self.negocio).esperar()
        if resultado is not None:
            self._cargar_grilla()

    def _editar(self):
        seleccionada = obtener_seleccion(self.tree, self.facturas_cargadas)
        if seleccionada is None:
            return

        try:
            detalles = self.negocio.listar_detalle(seleccionada["IdFactura"])
        except ErrorBaseDatos as ex:
            error(str(ex))
            return

        resultado = DialogoNuevaFactura(
            self,
            negocio=self.negocio,
            factura_existente=seleccionada,
            detalles_existentes=detalles,
        ).esperar()
        if resultado is not None:
            self._cargar_grilla()

    def _ver(self):
        seleccionada = obtener_seleccion(self.tree, self.facturas_cargadas)
        if seleccionada is None:
            return
        DialogoVerFactura(self, self.negocio, seleccionada).esperar()

    def _eliminar(self):
        seleccionada = obtener_seleccion(self.tree, self.facturas_cargadas)
        if seleccionada is None:
            return
        if not confirmar("Confirmar", "¿Eliminar factura?"):
            return

        try:
            self.negocio.eliminar(seleccionada["IdFactura"])
        except ErrorBaseDatos as ex:
            error(str(ex))
            return

        self._cargar_grilla()
