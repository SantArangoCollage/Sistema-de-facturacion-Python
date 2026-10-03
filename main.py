import tkinter as tk

from datos_sistema import cargar_datos_prueba
from capa_presentacion.pantalla_login import PantallaLogin
from pantalla_menu import PantallaMenu


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Facturación")
        self.geometry("1000x650")
        self.minsize(900, 600)

        self.pantalla_actual = None
        self.mostrar_login()

    def _cambiar_pantalla(self, nueva_pantalla: tk.Frame):
        if self.pantalla_actual is not None:
            self.pantalla_actual.destroy()
        self.pantalla_actual = nueva_pantalla
        self.pantalla_actual.pack(fill="both", expand=True)

    def mostrar_login(self):
        self._cambiar_pantalla(PantallaLogin(self, on_login_exitoso=self.mostrar_menu))

    def mostrar_menu(self):
        self._cambiar_pantalla(PantallaMenu(self, on_cerrar_sesion=self.mostrar_login))


def main():

    cargar_datos_prueba()

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
