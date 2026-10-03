"""
Capa de Negocio: valida los datos de un Producto y delega el acceso a
datos en ProductoDatos (Capa de Datos).
"""
from typing import List

from capa_datos.producto_datos import ProductoDatos
from capa_entidades.producto import Producto
from capa_negocio.manejo_errores import contexto_bd
from capa_negocio.validaciones import validar_categoria, validar_nombre_producto, validar_precio, validar_stock


class ProductoNegocio:
    def __init__(self):
        self.datos = ProductoDatos()

    def listar(self) -> List[dict]:
        with contexto_bd("No se pudieron consultar los productos"):
            return self.datos.consultar_todos()

    def validar(self, nombre, categoria, precio, stock) -> Producto:
        nombre = validar_nombre_producto(nombre)
        categoria = validar_categoria(categoria)
        precio = validar_precio(precio)
        stock = validar_stock(stock)
        return Producto(nombre=nombre, categoria=categoria, precio=precio, stock=stock)

    def crear(self, nombre: str, categoria: str, precio, stock) -> None:
        producto = self.validar(nombre, categoria, precio, stock)
        with contexto_bd("No se pudo guardar el producto"):
            self.datos.insertar(producto)

    def editar(self, id_producto: int, nombre: str, categoria: str, precio, stock) -> None:
        producto = self.validar(nombre, categoria, precio, stock)
        with contexto_bd("No se pudo actualizar el producto"):
            self.datos.actualizar(id_producto, producto)

    def eliminar(self, id_producto: int) -> None:
        with contexto_bd("No se pudo eliminar el producto"):
            self.datos.eliminar(id_producto)

    def ajustar_stock(self, id_producto: int, delta: int) -> None:
        """Suma (o resta, si 'delta' es negativo) unidades al stock de
        un producto. La usa FacturaNegocio al guardar, editar o
        eliminar una factura, para que el stock en BD quede siempre
        sincronizado con lo realmente facturado."""
        with contexto_bd("No se pudo actualizar el stock del producto"):
            self.datos.ajustar_stock(id_producto, delta)
