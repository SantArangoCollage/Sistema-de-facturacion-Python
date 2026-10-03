"""
Capa de Presentación: pantalla de inicio de sesión.

Ya NO ejecuta SQL directamente: valida las credenciales llamando a
UsuarioNegocio (Capa de Negocio), que a su vez usa UsuarioDatos
(Capa de Datos). Esta pantalla no sabe que existe SQL Server.
"""
import tkinter as tk
from tkinter import ttk

from acceso_datos import ErrorBaseDatos
from capa_negocio.usuario_negocio import UsuarioNegocio
from sesion import Sesion
from ui_common import COLOR_ACENTO, COLOR_BARRA, FUENTE_NORMAL, FUENTE_TITULO, error, info


class PantallaLogin(tk.Frame):
    def __init__(self, parent, on_login_exitoso):
        """
        parent: el contenedor (la ventana App)
        on_login_exitoso: callback que se llama cuando el login es correcto
        """
        super().__init__(parent, bg="white")
        self.on_login_exitoso = on_login_exitoso
        self.negocio = UsuarioNegocio()

        # Panel izquierdo decorativo
        panel_izquierdo = tk.Frame(self, bg=COLOR_BARRA, width=280)
        panel_izquierdo.pack(side="left", fill="y")
        panel_izquierdo.pack_propagate(False)

        tk.Label(
            panel_izquierdo,
            text="Sistema de\nFacturación",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg=COLOR_BARRA,
            justify="left",
        ).pack(padx=24, pady=(60, 10), anchor="w")

        tk.Label(
            panel_izquierdo,
            text="Ingresa tus credenciales\npara continuar",
            font=FUENTE_NORMAL,
            fg="#bdc3c7",
            bg=COLOR_BARRA,
            justify="left",
        ).pack(padx=24, anchor="w")

        # Panel derecho: formulario
        panel_derecho = tk.Frame(self, bg="white")
        panel_derecho.pack(side="left", fill="both", expand=True)

        contenedor = tk.Frame(panel_derecho, bg="white")
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(contenedor, text="Iniciar sesión", font=FUENTE_TITULO, bg="white").grid(
            row=0, column=0, columnspan=2, pady=(0, 20), sticky="w"
        )

        tk.Label(contenedor, text="Usuario", font=FUENTE_NORMAL, bg="white").grid(
            row=1, column=0, sticky="w", pady=6
        )
        self.txt_usuario = ttk.Entry(contenedor, width=28)
        self.txt_usuario.grid(row=1, column=1, pady=6, padx=(10, 0))

        tk.Label(contenedor, text="Contraseña", font=FUENTE_NORMAL, bg="white").grid(
            row=2, column=0, sticky="w", pady=6
        )
        self.txt_clave = ttk.Entry(contenedor, width=28, show="*")
        self.txt_clave.grid(row=2, column=1, pady=6, padx=(10, 0))

        btn_ingresar = tk.Button(
            contenedor,
            text="Ingresar",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_ACENTO,
            fg="white",
            relief="flat",
            padx=20,
            pady=6,
            command=self._intentar_ingresar,
            cursor="hand2",
        )
        btn_ingresar.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        self.txt_usuario.focus_set()
        self.txt_clave.bind("<Return>", lambda e: self._intentar_ingresar())

    def _intentar_ingresar(self):
        usuario_texto = self.txt_usuario.get().strip()
        clave_texto = self.txt_clave.get()

        try:
            fila = self.negocio.validar_credenciales(usuario_texto, clave_texto)
        except ErrorBaseDatos as ex:
            error(str(ex))
            return

        if fila is None:
            error("Usuario o contraseña incorrectos")
            return

        Sesion.id_usuario = fila["IdUsuario"]
        Sesion.usuario = fila["Usuario"]
        Sesion.nombre = fila["Nombre"]
        Sesion.rol = fila["Rol"]

        info(f"Bienvenido {Sesion.usuario}")
        self.on_login_exitoso()
