from typing import List

from models import Categoria


class DatosSistema:
    categorias: List[Categoria] = []


def cargar_datos_prueba() -> None:
    """Datos de prueba en memoria (categorías). Todo lo demás vive en
    SQL Server y se crea con setup_db.sql."""

    DatosSistema.categorias.append(Categoria(nombre="Aseo personal"))
    DatosSistema.categorias.append(Categoria(nombre="Bebidas"))
    DatosSistema.categorias.append(Categoria(nombre="Tecnología"))
