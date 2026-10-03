# Sistema de Facturación (versión Python / Tkinter)

# Diagrama mental

main.py
  └── PantallaLogin   (capa_presentacion -> UsuarioNegocio -> UsuarioDatos -> SQL Server)
        └── PantallaMenu (panel lateral)
              ├── Clientes   -> capa_presentacion/capa_negocio/capa_datos -> SQL Server
              ├── Productos  -> ídem -> SQL Server
              ├── Empleados  -> ídem -> SQL Server
              ├── Seguridad  -> ídem -> SQL Server
              ├── Facturas   -> ídem (+ reutiliza Cliente/Producto/Empleado Negocio) -> SQL Server
              ├── Categorías -> memoria (DatosSistema)
              └── Informes   -> consulta cada Negocio

# Correcta ejecucion del proyecto

# Antes de iniciar el proyecto configure primero:
 Python 3.10+ instalado, SQL Server corriendo (puede ser SQL Server Express) y el 'ODBC Driver 17 for SQL Server' instalado en tu equipo (se descarga de la página de Microsoft, no es un paquete de Python). Si usas SQL Server Management Studio (SSMS), asegúrate de poder conectarte con él primero — eso confirma que el servidor está accesible.

# Descomprime el proyecto
  Extrae el .zip que te compartí en una carpeta.  Ahí verás todos los archivos .py, el setup_db.sql y el README.md.

#  Crea la base de datos
  Abre SQL Server Management Studio (o la herramienta que uses para conectarte a tu servidor), abre el archivo 'setup_db.sql' y ejecútalo.

# Configura la conexión en config_db.py
  Abre 'config_db.py' con cualquier editor de texto y ajusta el valor de SERVIDOR con el nombre de tu instancia de SQL Server. Si te conectas con usuario y contraseña de SQL Server (no con tu usuario de Windows), cambia USAR_AUTENTICACION_WINDOWS a 'false' y completa USUARIO_DB y CLAVE_DB.

# Instala las dependencias de Python
  Abre una terminal dentro de la carpeta del proyecto y ejecuta: pip install -r requirements.txt — esto instala pyodbc, la librería que permite a Python hablar con SQL Server.

# Ejecuta la aplicación  
  ejecuta: python main.py debería abrirse la ventana de login del sistema.

# Inicia sesión y prueba 
  Ingresa con usuario 'admin' y contraseña '1234' 

# Configuraciones adicionales
capa_entidades/     -> Cliente, Producto, Factura, DetalleFactura (+ Empleado, Usuario de antes)
capa_datos/         -> ClienteDatos, ProductoDatos, FacturaDatos (+ EmpleadoDatos, UsuarioDatos)
capa_negocio/       -> ClienteNegocio, ProductoNegocio, FacturaNegocio, manejo_errores.py (nuevo)
capa_presentacion/  -> pantalla_clientes.py, pantalla_productos.py, pantalla_facturas.py (movidas)

cada capa solo conoce a la de abajo. La Presentación nunca ejecuta SQL ni conoce pyodbc; la Negocio nunca construye widgets de Tkinter; la Datos nunca decide si un dato es válido, solo lo guarda o lo consulta.