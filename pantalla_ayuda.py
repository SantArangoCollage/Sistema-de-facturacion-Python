import tkinter as tk

from ui_common import FUENTE_NORMAL, FUENTE_TITULO

TEXTO_AYUDA = """\
Guía rápida del sistema

- Clientes / Empleados: registra las personas con nombre, documento, \
dirección, teléfono y email.
- Categorías: agrupa los productos (ej. Bebidas, Aseo personal).
- Productos: define nombre, categoría, precio y stock.
- Facturas: selecciona un cliente y un empleado, agrega productos al \
detalle y guarda la factura. El IVA (19%) y el total se calculan \
automáticamente.
- Seguridad: administra los usuarios que pueden ingresar al sistema \
(Administrador o Cajero).
- Informes: consulta en una tabla los datos registrados por tipo.
"""


class PantallaAyuda(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white", padx=24, pady=24)

        tk.Label(self, text="Ayuda", font=FUENTE_TITULO, bg="white").pack(anchor="w", pady=(0, 12))
        tk.Label(
            self,
            text=TEXTO_AYUDA,
            font=FUENTE_NORMAL,
            bg="white",
            justify="left",
            anchor="w",
            wraplength=600,
        ).pack(anchor="w")
