import tkinter as tk
from tkinter import ttk

from capa_negocio.validaciones import (
    ErrorValidacion,
    validar_direccion,
    validar_documento,
    validar_email,
    validar_nombre,
    validar_telefono,
)
from ui_common import DialogoBase, FUENTE_NORMAL, error


class DialogoPersona(DialogoBase):
    def __init__(self, parent, titulo: str, persona=None):
        """
        persona: instancia existente a editar, o None para crear una nueva.
        Al guardar, self.resultado será un dict con los campos capturados.
        """
        super().__init__(parent, titulo)
        self.persona = persona

        campos = [
            ("nombre", "Nombre"),
            ("documento", "Documento"),
            ("direccion", "Dirección"),
            ("telefono", "Teléfono"),
            ("email", "Email"),
        ]

        self.entradas = {}
        for fila, (clave, etiqueta) in enumerate(campos):
            tk.Label(self, text=etiqueta, font=FUENTE_NORMAL).grid(
                row=fila, column=0, sticky="w", pady=4
            )
            entrada = ttk.Entry(self, width=32)
            entrada.grid(row=fila, column=1, pady=4, padx=(10, 0))
            self.entradas[clave] = entrada

        if persona is not None:
            self.entradas["nombre"].insert(0, persona.nombre)
            self.entradas["documento"].insert(0, persona.documento)
            self.entradas["direccion"].insert(0, persona.direccion)
            self.entradas["telefono"].insert(0, persona.telefono)
            self.entradas["email"].insert(0, persona.email)

        botones = tk.Frame(self)
        botones.grid(row=len(campos), column=0, columnspan=2, pady=(16, 0))

        tk.Button(botones, text="Guardar", width=12, command=self._guardar).pack(
            side="left", padx=4
        )
        tk.Button(
            botones, text="Salir", width=12, command=lambda: self.cerrar_con_resultado(None)
        ).pack(side="left", padx=4)

        self.entradas["nombre"].focus_set()

    def _guardar(self):
        crudo = {clave: entrada.get().strip() for clave, entrada in self.entradas.items()}

        try:
            datos = {
                "nombre": validar_nombre(crudo["nombre"]),
                "documento": validar_documento(crudo["documento"]),
                "telefono": validar_telefono(crudo["telefono"]),
                "direccion": validar_direccion(crudo["direccion"]),
                "email": validar_email(crudo["email"]),
            }
        except ErrorValidacion as ex:
            error(str(ex))
            return

        self.cerrar_con_resultado(datos)
