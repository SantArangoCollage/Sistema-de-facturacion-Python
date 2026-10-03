"""
Capa de Negocio: valida y arma una Factura completa (encabezado +
detalle) y delega el guardado en FacturaDatos (Capa de Datos).

Esta clase también sirve de punto único para que la Capa de
Presentación obtenga los Clientes, Productos y Empleados que necesita
para los combobox del formulario de factura — reutilizando las
Capas de Negocio de cada uno (así la validación/consulta de esos tres
siempre pasa por el mismo camino, sin importar desde qué pantalla se
pida).
"""
from typing import List

from capa_datos.factura_datos import FacturaDatos
from capa_entidades.cliente import Cliente
from capa_entidades.detalle_factura import DetalleFactura
from capa_entidades.empleado import Empleado
from capa_entidades.factura import Factura
from capa_entidades.producto import Producto
from capa_negocio.cliente_negocio import ClienteNegocio
from capa_negocio.empleado_negocio import EmpleadoNegocio
from capa_negocio.manejo_errores import contexto_bd
from capa_negocio.producto_negocio import ProductoNegocio
from capa_negocio.validaciones import ErrorValidacion, validar_cantidad, validar_descuento

PORCENTAJE_IVA = 0.19
ESTADOS_VALIDOS = ["Pendiente", "Pagada"]


class FacturaNegocio:
    def __init__(self):
        self.datos = FacturaDatos()
        self.cliente_negocio = ClienteNegocio()
        self.producto_negocio = ProductoNegocio()
        self.empleado_negocio = EmpleadoNegocio()

    def listar(self) -> List[dict]:
        with contexto_bd("No se pudieron consultar las facturas"):
            return self.datos.consultar_todas()

    def listar_detalle(self, id_factura: int) -> List[dict]:
        with contexto_bd("No se pudo consultar el detalle de la factura"):
            return self.datos.consultar_detalle(id_factura)

    def obtener_clientes(self) -> List[Cliente]:
        filas = self.cliente_negocio.listar()
        return [
            Cliente(
                nombre=f["Nombre"],
                documento=f["Documento"],
                direccion=f["Direccion"],
                telefono=f["Telefono"],
                email=f["Email"],
                id_cliente=f["IdCliente"],
            )
            for f in filas
        ]

    def obtener_productos(self) -> List[Producto]:
        filas = self.producto_negocio.listar()
        return [
            Producto(
                nombre=f["Nombre"],
                categoria=f["Categoria"] or "",
                precio=float(f["Precio"]),
                stock=f["Stock"],
                id_producto=f["IdProducto"],
            )
            for f in filas
        ]

    def obtener_empleados(self) -> List[Empleado]:
        filas = self.empleado_negocio.listar()
        return [
            Empleado(
                nombre=f["Nombre"],
                documento=f["Documento"],
                direccion=f["Direccion"],
                telefono=f["Telefono"],
                email=f["Email"],
                id_empleado=f["IdEmpleado"],
            )
            for f in filas
        ]

    def validar_stock_disponible(self, producto: Producto, cantidad: int, ya_reservada: int = 0) -> None:
        """Verifica que la cantidad solicitada no supere el stock
        disponible del producto. 'ya_reservada' es la cantidad que ESE
        MISMO producto ya tiene en otras líneas de la factura que se
        está armando (para no dejar que, por ejemplo, dos líneas de
        "Mouse" de 6 unidades cada una pasen una por una la validación
        pero sumen 12 contra un stock de 10)."""
        disponible = producto.stock - ya_reservada
        if cantidad > disponible:
            raise ErrorValidacion(
                f"Stock insuficiente de '{producto.nombre}': disponible {disponible}, "
                f"solicitado {cantidad}"
            )

    def crear_detalle(self, producto: Producto, cantidad, ya_reservada: int = 0) -> DetalleFactura:
        cantidad = validar_cantidad(cantidad, campo="La cantidad")
        self.validar_stock_disponible(producto, cantidad, ya_reservada)
        return DetalleFactura(producto=producto, cantidad=cantidad, precio=producto.precio)

    def _validar_y_armar(
        self,
        cliente: Cliente,
        empleado: Empleado,
        estado: str,
        descuento,
        detalles: List[DetalleFactura],
        id_factura: int = None,
    ) -> Factura:
        if cliente is None:
            raise ErrorValidacion("Seleccione un cliente")
        if empleado is None:
            raise ErrorValidacion("Seleccione un empleado")
        if estado not in ESTADOS_VALIDOS:
            raise ErrorValidacion("Seleccione un estado válido")
        if not detalles:
            raise ErrorValidacion("Debe agregar al menos un producto")

        descuento = validar_descuento(descuento)

        factura = Factura(
            cliente=cliente,
            empleado=empleado,
            estado=estado,
            descuento=descuento,
            id_factura=id_factura,
        )
        factura.detalles = list(detalles)
        factura.iva = factura.subtotal * PORCENTAJE_IVA
        return factura

    def guardar(
        self,
        cliente: Cliente,
        empleado: Empleado,
        estado: str,
        descuento,
        detalles: List[DetalleFactura],
    ) -> int:
        factura = self._validar_y_armar(cliente, empleado, estado, descuento, detalles)
        with contexto_bd("No se pudo guardar la factura"):
            id_factura = self.datos.insertar(factura)
        self._descontar_stock(detalles)
        return id_factura

    def editar(
        self,
        id_factura: int,
        cliente: Cliente,
        empleado: Empleado,
        estado: str,
        descuento,
        detalles: List[DetalleFactura],
    ) -> None:
        """Actualiza una factura ya existente (encabezado + todas sus
        líneas de detalle), con las mismas validaciones que crear una
        nueva. El stock se reajusta: primero se devuelven las
        cantidades que tenía la factura ANTES de editarla, y luego se
        descuentan las cantidades nuevas — así el stock final siempre
        refleja exactamente lo que quedó facturado, sin importar si el
        usuario aumentó, redujo o cambió de producto una línea."""
        factura = self._validar_y_armar(
            cliente, empleado, estado, descuento, detalles, id_factura=id_factura
        )
        with contexto_bd("No se pudo actualizar la factura"):
            detalles_anteriores = self.datos.consultar_detalle(id_factura)
            self.datos.actualizar(factura)

        self._restaurar_stock_filas(detalles_anteriores)
        self._descontar_stock(detalles)

    def eliminar(self, id_factura: int) -> None:
        with contexto_bd("No se pudo eliminar la factura"):
            detalles_anteriores = self.datos.consultar_detalle(id_factura)
            self.datos.eliminar(id_factura)

        self._restaurar_stock_filas(detalles_anteriores)

    def _descontar_stock(self, detalles: List[DetalleFactura]) -> None:
        for detalle in detalles:
            self.producto_negocio.ajustar_stock(detalle.producto.id_producto, -detalle.cantidad)

    def _restaurar_stock_filas(self, filas_detalle: List[dict]) -> None:
        """Igual que '_descontar_stock', pero a partir de filas crudas
        de BD (lo que devuelve 'FacturaDatos.consultar_detalle'), y
        sumando en vez de restar — se usa al editar (para devolver lo
        que tenía la versión anterior) y al eliminar una factura."""
        for fila in filas_detalle:
            self.producto_negocio.ajustar_stock(fila["IdProducto"], fila["Cantidad"])
