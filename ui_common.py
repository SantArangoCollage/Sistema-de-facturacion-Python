import tkinter as tk
from tkinter import messagebox, ttk

FUENTE_TITULO = ("Segoe UI", 14, "bold")
FUENTE_NORMAL = ("Segoe UI", 10)
COLOR_BARRA = "#2c3e50"
COLOR_BARRA_TEXTO = "white"
COLOR_ACENTO = "#2980b9"


class DialogoBase(tk.Toplevel):
    """Ventana modal base para formularios de creación/edición.

    Uso:
        dlg = MiDialogo(parent, ...)
        resultado = dlg.esperar()   # None si se canceló
    """

    def __init__(self, parent, titulo: str):
        super().__init__(parent)
        self.title(titulo)
        self.resizable(False, False)
        self.resultado = None
        self.configure(padx=16, pady=16)
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._cancelar)

    def _cancelar(self):
        self.resultado = None
        self.destroy()

    def cerrar_con_resultado(self, resultado):
        self.resultado = resultado
        self.destroy()

    def esperar(self):
        self.wait_window()
        return self.resultado


def crear_treeview(parent, columnas):
    """Crea un Treeview (tabla) con scrollbar vertical.

    columnas: lista de tuplas (id, titulo, ancho)
    Devuelve (frame_contenedor, treeview)
    """
    frame = ttk.Frame(parent)
    tree = ttk.Treeview(
        frame,
        columns=[c[0] for c in columnas],
        show="headings",
        selectmode="browse",
    )
    for col_id, titulo, ancho in columnas:
        tree.heading(col_id, text=titulo)
        tree.column(col_id, width=ancho, anchor="w")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    return frame, tree


def obtener_seleccion(tree: ttk.Treeview, lista_datos: list):
    """
    Devuelve el objeto de 'lista_datos' asociado a la fila seleccionada
    del Treeview, o None si no hay selección.
    """
    seleccion = tree.selection()
    if not seleccion:
        return None
    indice = tree.index(seleccion[0])
    if indice < 0 or indice >= len(lista_datos):
        return None
    return lista_datos[indice]


def confirmar(titulo: str, mensaje: str) -> bool:
    return messagebox.askyesno(titulo, mensaje, icon="question")


def error(mensaje: str):
    messagebox.showerror("Atención", mensaje)


def info(mensaje: str):
    messagebox.showinfo("Información", mensaje)
