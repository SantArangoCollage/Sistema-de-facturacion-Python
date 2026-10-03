from typing import Any, Iterable, Optional

import pyodbc

from config_db import construir_cadena_conexion


class ErrorBaseDatos(Exception):
    """Error amigable para mostrar en la interfaz cuando falla la conexión."""


class AccesoDatos:
    def _conectar(self) -> pyodbc.Connection:
        try:
            return pyodbc.connect(construir_cadena_conexion())
        except pyodbc.Error as ex:
            raise ErrorBaseDatos(
                "No se pudo conectar a la base de datos.\n"
                "Verifica el servidor, el nombre de la base de datos y el "
                "driver ODBC en config_db.py.\n\nDetalle técnico: " + str(ex)
            ) from ex

    def ejecutar_consulta(
        self, sql: str, parametros: Optional[Iterable[Any]] = None
    ) -> list[dict]:
        conexion = self._conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, parametros or [])
            columnas = [col[0] for col in cursor.description]
            return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        except pyodbc.Error as ex:
            raise ErrorBaseDatos(f"Error al consultar la base de datos:\n{ex}") from ex
        finally:
            conexion.close()

    def ejecutar_comando(self, sql: str, parametros: Optional[Iterable[Any]] = None) -> None:
        conexion = self._conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, parametros or [])
            conexion.commit()
        except pyodbc.Error as ex:
            conexion.rollback()
            raise ErrorBaseDatos(f"Error al ejecutar el comando:\n{ex}") from ex
        finally:
            conexion.close()

    def ejecutar_insert_devolviendo_id(
        self, sql: str, parametros: Optional[Iterable[Any]] = None
    ) -> int:
        conexion = self._conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SET NOCOUNT ON; " + sql + "; SELECT CAST(SCOPE_IDENTITY() AS INT)",
                parametros or [],
            )
            fila = cursor.fetchone()
            nuevo_id = fila[0] if fila is not None else None
            if nuevo_id is None:
                # No debería pasar nunca: si llega aquí es que el INSERT
                # no generó un Id (por ejemplo, un trigger en la tabla
                # cambió el scope). Se reporta como error claro en vez
                # de dejar que el NULL falle más adelante en otra tabla.
                conexion.rollback()
                raise ErrorBaseDatos(
                    "No se pudo obtener el Id generado tras el INSERT "
                    "(SCOPE_IDENTITY devolvió NULL)."
                )
            conexion.commit()
            return nuevo_id
        except pyodbc.Error as ex:
            conexion.rollback()
            raise ErrorBaseDatos(f"Error al insertar el registro:\n{ex}") from ex
        finally:
            conexion.close()
