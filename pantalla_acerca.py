import tkinter as tk

from ui_common import DialogoBase, FUENTE_NORMAL, FUENTE_TITULO


class DialogoAcerca(DialogoBase):
    def __init__(self, parent):
        super().__init__(parent, "Acerca de")

        tk.Label(self, text="Sistema de Facturación", font=FUENTE_TITULO).pack(pady=(0, 8))
        tk.Label(
            self,
            text="Versión Python (Tkinter)\nRealizado por Santiago Arango Arbelaez.",
            font=FUENTE_NORMAL,
            justify="center",
        ).pack(pady=(0, 16))

        tk.Button(self, text="Cerrar", command=lambda: self.cerrar_con_resultado(None)).pack()


def mostrar_acerca(parent):
    DialogoAcerca(parent).esperar()
