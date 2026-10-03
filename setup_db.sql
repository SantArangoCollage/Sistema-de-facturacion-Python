IF DB_ID('SistemaVentas') IS NULL
BEGIN
    CREATE DATABASE SistemaVentas;
END
GO

USE SistemaVentas;
GO

IF OBJECT_ID('dbo.Clientes', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Clientes (
        IdCliente   INT IDENTITY(1,1) PRIMARY KEY,
        Nombre      NVARCHAR(150) NOT NULL,
        Documento   NVARCHAR(50)  NULL,
        Telefono    NVARCHAR(50)  NULL,
        Direccion   NVARCHAR(200) NULL,
        Email       NVARCHAR(150) NULL
    );
END
GO

IF OBJECT_ID('dbo.Productos', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Productos (
        IdProducto  INT IDENTITY(1,1) PRIMARY KEY,
        Nombre      NVARCHAR(150) NOT NULL,
        Categoria   NVARCHAR(100) NULL,
        Precio      DECIMAL(12,2) NOT NULL DEFAULT 0,
        Stock       INT NOT NULL DEFAULT 0
    );
END
GO

IF OBJECT_ID('dbo.Usuarios', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Usuarios (
        IdUsuario   INT IDENTITY(1,1) PRIMARY KEY,
        Nombre      NVARCHAR(150) NOT NULL,
        Usuario     NVARCHAR(50)  NOT NULL UNIQUE,
        Password    NVARCHAR(100) NOT NULL,
        Rol         NVARCHAR(30)  NOT NULL DEFAULT 'Cajero'
    );
END
GO

IF OBJECT_ID('dbo.Empleados', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Empleados (
        IdEmpleado  INT IDENTITY(1,1) PRIMARY KEY,
        Nombre      NVARCHAR(150) NOT NULL,
        Documento   NVARCHAR(50)  NULL,
        Telefono    NVARCHAR(50)  NULL,
        Direccion   NVARCHAR(200) NULL,
        Email       NVARCHAR(150) NULL
    );
END
GO

IF OBJECT_ID('dbo.Facturas', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Facturas (
        IdFactura     INT IDENTITY(1,1) PRIMARY KEY,
        IdCliente     INT NOT NULL REFERENCES dbo.Clientes(IdCliente),
        IdEmpleado    INT NOT NULL REFERENCES dbo.Empleados(IdEmpleado),
        FechaRegistro DATETIME NOT NULL DEFAULT GETDATE(),
        Estado        NVARCHAR(30) NOT NULL DEFAULT 'Pendiente',
        Descuento     DECIMAL(12,2) NOT NULL DEFAULT 0,
        Iva           DECIMAL(12,2) NOT NULL DEFAULT 0
    );
END
GO

IF OBJECT_ID('dbo.DetalleFactura', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.DetalleFactura (
        IdDetalle   INT IDENTITY(1,1) PRIMARY KEY,
        IdFactura   INT NOT NULL REFERENCES dbo.Facturas(IdFactura) ON DELETE CASCADE,
        IdProducto  INT NOT NULL REFERENCES dbo.Productos(IdProducto),
        Cantidad    INT NOT NULL,
        Precio      DECIMAL(12,2) NOT NULL
    );
END
GO


IF NOT EXISTS (SELECT 1 FROM dbo.Usuarios WHERE Usuario = 'admin')
BEGIN
    INSERT INTO dbo.Usuarios (Nombre, Usuario, Password, Rol)
    VALUES ('Administrador', 'admin', '1234', 'Administrador');
END
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Productos WHERE Nombre = 'Shampoo')
BEGIN
    INSERT INTO dbo.Productos (Nombre, Categoria, Precio, Stock)
    VALUES ('Shampoo', 'Aseo personal', 30000, 10);
END
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Productos WHERE Nombre = 'Gaseosa')
BEGIN
    INSERT INTO dbo.Productos (Nombre, Categoria, Precio, Stock)
    VALUES ('Gaseosa', 'Bebidas', 5000, 20);
END
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Empleados WHERE Documento = '1000000000')
BEGIN
    INSERT INTO dbo.Empleados (Nombre, Documento, Telefono, Direccion, Email)
    VALUES ('Empleado de Prueba', '1000000000', '3000000000', 'Calle 1', 'empleado@prueba.com');
END
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Clientes WHERE Documento = '2000000000')
BEGIN
    INSERT INTO dbo.Clientes (Nombre, Documento, Telefono, Direccion, Email)
    VALUES ('Cliente de Prueba', '2000000000', '3109999999', 'Calle 2', 'cliente@prueba.com');
END
GO


SELECT * FROM Productos;

SELECT * FROM Clientes;

SELECT * FROM Usuarios;

SELECT * FROM Empleados;

SELECT * FROM Facturas;

SELECT * FROM DetalleFactura;