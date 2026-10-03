import tkinter as tk
from tkinter import ttk

from datos_sistema import DatosSistema
from models import Categoria
from ui_common import (
    DialogoBase,
    FUENTE_NORMAL,
    FUENTE_TITULO,
    confirmar,
    crear_treeview,
    error,
    obtener_seleccion,
)


class DialogoCategoria(DialogoBase):
    def __init__(self, parent, categoria: Categoria = None):
        titulo = "Editar categoría" if categoria else "Nueva categoría"
        super().__init__(parent, titulo)
        self.categoria = categoria

        tk.Label(self, text="Nombre", font=FUENTE_NORMAL).grid(row=0, column=0, sticky="w", pady=4)
        self.txt_nombre = ttk.Entry(self, width=32)
        self.txt_nombre.grid(row=0, column=1, pady=4, padx=(10, 0))

        tk.Label(self, text="Descripción", font=FUENTE_NORMAL).grid(
            row=1, column=0, sticky="w", pady=4
        )
        self.txt_descripcion = ttk.Entry(self, width=32)
        self.txt_descripcion.grid(row=1, column=1, pady=4, padx=(10, 0))

        if categoria is not None:
            self.txt_nombre.insert(0, categoria.nombre)
            self.txt_descripcion.insert(0, categoria.descripcion)

        botones = tk.Frame(self)
        botones.grid(row=2, column=0, columnspan=2, pady=(16, 0))
        tk.Button(botones, text="Guardar", width=12, command=self._guardar).pack(
            side="left", padx=4
        )
        tk.Button(
            botones, text="Salir", width=12, command=lambda: self.cerrar_con_resultado(None)
        ).pack(side="left", padx=4)

        self.txt_nombre.focus_set()

    def _guardar(self):
        nombre = self.txt_nombre.get().strip()
        if not nombre:
            error("El nombre es obligatorio")
            return
        self.cerrar_con_resultado(
            {"nombre": nombre, "descripcion": self.txt_descripcion.get().strip()}
        )


class PantallaListaCategorias(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white", padx=16, pady=16)

        tk.Label(self, text="Categorías", font=FUENTE_TITULO, bg="white").pack(
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

        columnas = [("nombre", "Nombre", 200), ("descripcion", "Descripción", 300)]
        frame_tabla, self.tree = crear_treeview(self, columnas)
        frame_tabla.pack(fill="both", expand=True)

        self._cargar_grilla()

    def _cargar_grilla(self):
        self.tree.delete(*self.tree.get_children())
        for categoria in DatosSistema.categorias:
            self.tree.insert("", "end", values=(categoria.nombre, categoria.descripcion))

    def _nuevo(self):
        datos = DialogoCategoria(self).esperar()
        if datos is None:
            return
        DatosSistema.categorias.append(Categoria(**datos))
        self._cargar_grilla()

    def _editar(self):
        seleccionado = obtener_seleccion(self.tree, DatosSistema.categorias)
        if seleccionado is None:
            return
        datos = DialogoCategoria(self, categoria=seleccionado).esperar()
        if datos is None:
            return
        seleccionado.nombre = datos["nombre"]
        seleccionado.descripcion = datos["descripcion"]
        self._cargar_grilla()

    def _eliminar(self):
        # Nota: como Productos.Categoria ahora vive en SQL Server y se
        # guarda como texto (sin relación formal con esta lista en
        # memoria), aquí ya no se valida contra productos existentes.
        seleccionado = obtener_seleccion(self.tree, DatosSistema.categorias)
        if seleccionado is None:
            return
        if confirmar("Confirmar", "¿Eliminar categoría?"):
            DatosSistema.categorias.remove(seleccionado)
            self._cargar_grilla()
