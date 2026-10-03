"""Menú principal con panel lateral."""
import tkinter as tk

from pantalla_acerca import mostrar_acerca
from pantalla_ayuda import PantallaAyuda
from pantalla_categorias import PantallaListaCategorias
from capa_presentacion.pantalla_clientes import PantallaListaClientes
from capa_presentacion.pantalla_empleados import PantallaListaEmpleados
from capa_presentacion.pantalla_facturas import PantallaListaFacturas
from pantalla_informes import PantallaInformes
from capa_presentacion.pantalla_productos import PantallaListaProductos
from capa_presentacion.pantalla_usuarios import PantallaListaUsuarios
from sesion import Sesion
from ui_common import COLOR_BARRA

COLOR_BOTON_HOVER = "#34495e"


class PantallaMenu(tk.Frame):
    def __init__(self, parent, on_cerrar_sesion):
        super().__init__(parent, bg="white")

        self.on_cerrar_sesion = on_cerrar_sesion
        self.formulario_activo = None

        # ---- Panel lateral ----
        pnl_menu = tk.Frame(self, bg=COLOR_BARRA, width=220)
        pnl_menu.pack(side="left", fill="y")
        pnl_menu.pack_propagate(False)

        nombre_usuario = Sesion.nombre or Sesion.usuario or "Invitado"
        rol_usuario = Sesion.rol or ""

        tk.Label(
            pnl_menu,
            text="Sistema de\nFacturación",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg=COLOR_BARRA,
            justify="left",
        ).pack(padx=16, pady=(20, 4), anchor="w")

        tk.Label(
            pnl_menu,
            text=f"{nombre_usuario} ({rol_usuario})",
            font=("Segoe UI", 8),
            fg="#bdc3c7",
            bg=COLOR_BARRA,
            justify="left",
            wraplength=190,
        ).pack(padx=16, pady=(0, 20), anchor="w")

        botones = [
            ("Clientes", lambda: self.abrir_formulario(PantallaListaClientes)),
            ("Productos", lambda: self.abrir_formulario(PantallaListaProductos)),
            ("Categorías", lambda: self.abrir_formulario(PantallaListaCategorias)),
            ("Facturas", lambda: self.abrir_formulario(PantallaListaFacturas)),
            ("Empleados", lambda: self.abrir_formulario(PantallaListaEmpleados)),
            ("Seguridad", lambda: self.abrir_formulario(PantallaListaUsuarios)),
            ("Informes", lambda: self.abrir_formulario(PantallaInformes)),
            ("Ayuda", lambda: self.abrir_formulario(PantallaAyuda)),
            ("Acerca de", lambda: mostrar_acerca(self)),
        ]

        for texto, comando in botones:
            self._crear_boton_menu(pnl_menu, texto, comando)

        # Separador visual antes de "Cerrar sesión"
        tk.Frame(pnl_menu, bg="#3d566e", height=1).pack(fill="x", pady=10)
        self._crear_boton_menu(pnl_menu, "Cerrar sesión", self._cerrar_sesion)

        # ---- Contenedor de la pantalla activa ----
        self.pnl_contenedor = tk.Frame(self, bg="#ecf0f1")
        self.pnl_contenedor.pack(side="left", fill="both", expand=True)

        tk.Label(
            self.pnl_contenedor,
            text="Selecciona una opción del menú",
            font=("Segoe UI", 12),
            bg="#ecf0f1",
            fg="#7f8c8d",
        ).pack(expand=True)

    def _crear_boton_menu(self, parent, texto, comando):
        btn = tk.Button(
            parent,
            text=texto,
            font=("Segoe UI", 10),
            bg=COLOR_BARRA,
            fg="white",
            activebackground=COLOR_BOTON_HOVER,
            activeforeground="white",
            relief="flat",
            anchor="w",
            padx=16,
            pady=10,
            bd=0,
            command=comando,
            cursor="hand2",
        )
        btn.pack(fill="x")
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_BOTON_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_BARRA))
        return btn

    def abrir_formulario(self, clase_formulario):
        if self.formulario_activo is not None:
            self.formulario_activo.destroy()

        self.formulario_activo = clase_formulario(self.pnl_contenedor)
        self.formulario_activo.pack(fill="both", expand=True)

    def _cerrar_sesion(self):
        Sesion.cerrar()
        self.on_cerrar_sesion()
