import os

SERVIDOR = os.environ.get("FACTURACION_DB_SERVIDOR", "localhost")

BASE_DATOS = os.environ.get("FACTURACION_DB_NOMBRE", "SistemaVentas")

USAR_AUTENTICACION_WINDOWS = os.environ.get(
    "FACTURACION_DB_WINDOWS_AUTH", "true"
).lower() in ("1", "true", "yes")

USUARIO_DB = os.environ.get("FACTURACION_DB_USUARIO", "")
CLAVE_DB = os.environ.get("FACTURACION_DB_CLAVE", "")

DRIVER_ODBC = os.environ.get("FACTURACION_DB_DRIVER", "ODBC Driver 17 for SQL Server")


def construir_cadena_conexion() -> str:
    partes = [
        f"DRIVER={{{DRIVER_ODBC}}}",
        f"SERVER={SERVIDOR}",
        f"DATABASE={BASE_DATOS}",
    ]
    if USAR_AUTENTICACION_WINDOWS:
        partes.append("Trusted_Connection=yes")
    else:
        partes.append(f"UID={USUARIO_DB}")
        partes.append(f"PWD={CLAVE_DB}")

    return ";".join(partes) + ";"
