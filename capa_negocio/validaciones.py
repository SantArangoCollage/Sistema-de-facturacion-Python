"""
Capa de Negocio: reglas de validación reutilizables.

Estas funciones NO acceden a la base de datos ni a la interfaz — solo
verifican que un valor cumpla las reglas del negocio. Si algo no es
válido, lanzan ErrorValidacion con un mensaje listo para mostrarle al
usuario. La Capa de Presentación solo necesita atrapar esa excepción.
"""
import re

PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")


class ErrorValidacion(Exception):
    """Un dato no cumple una regla de negocio. Nunca llega a tocar la base de datos."""


def validar_nombre(valor: str, campo: str = "El nombre") -> str:
    valor = (valor or "").strip()
    if not valor:
        raise ErrorValidacion(f"{campo} es obligatorio")
    if len(valor) > 100:
        raise ErrorValidacion(f"{campo} no puede superar los 100 caracteres")
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÑÜáéíóúñü ]+", valor):
        raise ErrorValidacion(f"{campo} solo puede contener letras y espacios (sin números ni símbolos)")
    return valor


def validar_documento(valor: str) -> str:
    valor = (valor or "").strip()
    if not valor:
        raise ErrorValidacion("El documento es obligatorio")
    if not valor.isdigit():
        raise ErrorValidacion("El documento solo puede contener números")
    if not (5 <= len(valor) <= 15):
        raise ErrorValidacion("El documento debe tener entre 5 y 15 dígitos")
    return valor


def validar_telefono(valor: str) -> str:
    valor = (valor or "").strip()
    if not valor:
        raise ErrorValidacion("El teléfono es obligatorio")
    if not valor.isdigit():
        raise ErrorValidacion("El teléfono solo puede contener números")
    if not (7 <= len(valor) <= 10):
        raise ErrorValidacion("El teléfono debe tener entre 7 y 10 dígitos")
    return valor


def validar_email(valor: str) -> str:
    valor = (valor or "").strip()
    if not valor:
        raise ErrorValidacion("El email es obligatorio")
    if not PATRON_EMAIL.fullmatch(valor):
        raise ErrorValidacion("El email no tiene un formato válido (ejemplo: nombre@dominio.com)")
    return valor


def validar_direccion(valor: str) -> str:
    valor = (valor or "").strip()
    if not valor:
        raise ErrorValidacion("La dirección es obligatoria")
    if len(valor) > 200:
        raise ErrorValidacion("La dirección no puede superar los 200 caracteres")
    return valor


def validar_nombre_producto(valor: str) -> str:
    """Más permisivo que validar_nombre: un producto sí puede llevar
    números en el nombre (ej. 'iPhone 13'), pero no puede ser SOLO
    números, ni quedar vacío."""
    valor = (valor or "").strip()
    if not valor:
        raise ErrorValidacion("El nombre es obligatorio")
    if len(valor) > 100:
        raise ErrorValidacion("El nombre no puede superar los 100 caracteres")
    if valor.replace(" ", "").isdigit():
        raise ErrorValidacion("El nombre no puede ser solo números")
    return valor


def validar_categoria(valor: str) -> str:
    valor = (valor or "").strip()
    if not valor:
        raise ErrorValidacion("Seleccione una categoría")
    return valor


PRECIO_MAXIMO = 999_999_999.99


def validar_precio(valor, maximo: float = PRECIO_MAXIMO) -> float:
    try:
        precio = float(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion("El precio debe ser un número válido")
    if precio <= 0:
        raise ErrorValidacion("El precio debe ser mayor a 0")
    if precio > maximo:
        raise ErrorValidacion(f"El precio no puede superar {maximo:,.2f}")
    return round(precio, 2)


def validar_stock(valor) -> int:
    try:
        stock = int(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion("El stock debe ser un número entero válido")
    if stock < 0:
        raise ErrorValidacion("El stock no puede ser negativo")
    return stock


def validar_cantidad(valor, campo: str = "La cantidad") -> int:
    try:
        cantidad = int(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion(f"{campo} debe ser un número entero válido")
    if cantidad <= 0:
        raise ErrorValidacion(f"{campo} debe ser mayor a 0")
    return cantidad


def validar_descuento(valor, maximo: float = PRECIO_MAXIMO) -> float:
    try:
        descuento = float(valor or 0)
    except (TypeError, ValueError):
        raise ErrorValidacion("El descuento debe ser un número válido")
    if descuento < 0:
        raise ErrorValidacion("El descuento no puede ser negativo")
    if descuento > maximo:
        raise ErrorValidacion(f"El descuento no puede superar {maximo:,.2f}")
    return round(descuento, 2)
