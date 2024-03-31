DROP DATABASE IF EXISTS cookiesInc;
CREATE DATABASE cookiesInc;

USE cookiesInc;

-- --------------------------
-- ----- USUARIO ------------
-- --------------------------

CREATE TABLE tipousuario (
    id_tipousuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(50) NOT NULL,
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT NOT NULL,
    fecha_registro DATETIME NOT NULL
);

CREATE TABLE menu (
    id_menu INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_menu VARCHAR(50) NOT NULL,
    enlace VARCHAR(200),
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT NOT NULL,
    fecha_registro DATETIME NOT NULL
);

CREATE TABLE usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tipousuarioid_usua INT NOT NULL,
    nombrecompleto_usuario VARCHAR(70) NOT NULL,
    fecha_nacimiento DATE,
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT NOT NULL,
    fecha_registro DATETIME NOT NULL,
    CONSTRAINT fk_tipousuarioid_usua FOREIGN KEY (tipousuarioid_usua) REFERENCES tipousuario(id_tipousuario)
);

CREATE TABLE menu_tipousuario (
    tipousuarioid_mt INT NOT NULL,
    menuid_mt INT NOT NULL,
    estatus BIT NOT NULL DEFAULT 1,
    CONSTRAINT fk_tipousuarioid_mt FOREIGN KEY (tipousuarioid_mt) REFERENCES tipousuario(id_tipousuario),
    CONSTRAINT fk_menuid_mt FOREIGN KEY (menuid_mt) REFERENCES menu(id_menu)
);

-- --------------------------
-- ----- CLIENTE ------------
-- --------------------------

CREATE TABLE cliente (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    antiguedad DATETIME,
    nombre_cliente VARCHAR(50),
    correo VARCHAR(50),
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro VARCHAR(50),
    fecha_registro DATETIME
);

-- --------------------------
-- -------- VENTA -----------
-- --------------------------

CREATE TABLE venta (
    id_venta INT PRIMARY KEY AUTO_INCREMENT,
    cliente_venta INT NOT NULL,
    usuario_venta INT NOT NULL,
    folio_venta VARCHAR(50),
    fecha_venta DATE,
    fecha_cancelacion DATE,
    cantidad_productos INT,
    total_ventas DOUBLE,
    estatus BIT NOT NULL DEFAULT 1,
    fecha_registro DATETIME,
    CONSTRAINT fk_cliente_venta FOREIGN KEY (cliente_venta) REFERENCES cliente(id_cliente),
    CONSTRAINT fk_usuario_venta FOREIGN KEY (usuario_venta) REFERENCES usuario(id_usuario)
);

CREATE TABLE producto (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_pd VARCHAR(50),
    alias VARCHAR(50),
    dias_caducidad INT,
    unidad_medida VARCHAR(10),
    costo_producto DOUBLE,
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT,
    fecha_registro DATETIME
);

DROP TABLE IF EXISTS ventaitem;
CREATE TABLE ventaitem (
    id_ventaitem INT PRIMARY KEY AUTO_INCREMENT,
    venta_itm INT NOT NULL,
    producto_itm INT NOT NULL,
    cantidad INT,
    subtotal DOUBLE,
    descuento DOUBLE,
    total DOUBLE,
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT,
    fecha_registro DATETIME,
    CONSTRAINT fk_venta_itm FOREIGN KEY (venta_itm) REFERENCES venta(id_venta),
    CONSTRAINT fk_producto_itm FOREIGN KEY (producto_itm) REFERENCES producto(id_producto)
);

CREATE TABLE receta (
    id_receta INT PRIMARY KEY AUTO_INCREMENT,
    nombre_receta VARCHAR(50),
    alias VARCHAR(50),
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT,
    fecha_registro DATETIME
);

CREATE TABLE recetaitem (
    id_recetaitem INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    recetaid_itm INT NOT NULL,
    materialid_itm INT NOT NULL,
    cantidad_requerida DOUBLE,
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT,
    fecha_registro DATETIME
);

-- --------------------------
-- ----- MATERIAL -----------
-- --------------------------

CREATE TABLE material (
    id_material INT PRIMARY KEY AUTO_INCREMENT,
    nombre_mat VARCHAR(15),
    dias_caducidad DATETIME,
    unidad_medida VARCHAR(50),
    costo_mat DOUBLE,
    estatus BIT NOT NULL DEFAULT 1,
    fecha_registro DATETIME
);

-- --------------------------
-- ----- PROVEEDOR ----------
-- --------------------------

CREATE TABLE proveedor (
    id_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50),
    telefono VARCHAR(20),
    correo VARCHAR(20),
    dias_visita VARCHAR(50),
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT,
    fecha_registro DATETIME
);

-- --------------------------
-- ----- INVENTARIO ---------
-- --------------------------
CREATE TABLE tipostock (
    id_tipostock INT PRIMARY KEY AUTO_INCREMENT,
    nombre_stock VARCHAR(50),
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT,
    fecha_registro DATETIME
);

CREATE TABLE tipoinventario (
    id_tipoInventario INT PRIMARY KEY AUTO_INCREMENT,
    nombre_tipoInv VARCHAR(50),
    estatus BIT NOT NULL DEFAULT 1,
    usuarios_registro INT,
    fecha_registro DATETIME
);

DROP TABLE if exists inventario;
CREATE TABLE inventario (
    id_inventario INT PRIMARY KEY AUTO_INCREMENT,
    tipostock_inv INT NOT NULL,
    producto_inv INT NOT NULL,
    material_inv INT NOT NULL,
    tipo_inv INT NOT NULL,
    fecha_caducidad DATE,
    proveedorid_inv INT,
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT,
    fecha_registro DATETIME,
    CONSTRAINT fk_tipostock_inv FOREIGN KEY (tipostock_inv) REFERENCES tipostock(id_tipostock),
    CONSTRAINT fk_producto_inv FOREIGN KEY (producto_inv) REFERENCES producto(id_producto),
    CONSTRAINT fk_material_inv FOREIGN KEY (material_inv) REFERENCES material(id_material),
    CONSTRAINT fk_tipo_inv FOREIGN KEY (tipo_inv) REFERENCES tipoinventario(id_tipoInventario),
    CONSTRAINT fk_proveedor_inv FOREIGN KEY (proveedorid_inv) REFERENCES proveedor(id_proveedor)
);

-- --------------------------
-- ----- PRODUCCION ---------
-- --------------------------
drop table if exists produccion;
CREATE TABLE produccion (
    id_produccion INT PRIMARY KEY AUTO_INCREMENT,
    usuarioid_produce_prd INT NOT NULL,
    usuarioid_solicito_prd INT NOT NULL,
    folio_produccion VARCHAR(50),
    fecha_inicio DATETIME,
    fecha_fin DATETIME,
    cantidad_total DOUBLE,
    costo_total DOUBLE,
    estatus BIT NOT NULL DEFAULT 1,
    fecha_registro DATETIME
);

drop table if exists produccionitem;
CREATE TABLE produccionitem (
    id_produccionitem INT PRIMARY KEY AUTO_INCREMENT,
    produccion_itm INT NOT NULL,
    producto_itm INT NOT NULL,
    cantidad INT,
    costo DOUBLE,
    estarus BIT NOT NULL DEFAULT 1,
    usuario_registrado INT,
    fecha_registro DATETIME,
    CONSTRAINT fk_produccion_itm FOREIGN KEY (produccion_itm) REFERENCES produccion(id_produccion),
    CONSTRAINT fk_producto_itm_produccionitem FOREIGN KEY (producto_itm) REFERENCES producto(id_producto)
);

-- --------------------------
-- ----- COMPRA -------------
-- --------------------------

CREATE TABLE compra (
    id_compra INT PRIMARY KEY AUTO_INCREMENT,
    proveedorid_comp INT NOT NULL,
    usuario_comp INT,
    folio_comp VARCHAR(50),
    fecha_comp DATETIME,
    fecha_cancelacion DATETIME,
    cantidad INT,
    total DOUBLE,
    estaus BIT NOT NULL DEFAULT 1,
    fecha_registro DATETIME,
    CONSTRAINT fk_proveedorid_comp FOREIGN KEY (proveedorid_comp) REFERENCES proveedor(id_proveedor),
    CONSTRAINT fk_usuario_comp FOREIGN KEY (usuario_comp) REFERENCES usuario(id_usuario)
);

CREATE TABLE compraitem (
    id_compraitem INT PRIMARY KEY AUTO_INCREMENT,
    compra_itm INT NOT NULL,
    materialid_itm INT NOT NULL,
    cantidad INT,
    subtotal DOUBLE,
    descuento DOUBLE,
    total DOUBLE,
    estatus BIT NOT NULL DEFAULT 1,
    usuario_registro INT,
    fecha_registro DATETIME,
    CONSTRAINT fk_compra_itm FOREIGN KEY (compra_itm) REFERENCES compra(id_compra),
    CONSTRAINT fk_materialid_itm FOREIGN KEY (materialid_itm) REFERENCES material(id_material)
);

-- -----------------------------INSERTS--------------------------------------------------------------------------

-- Inserts for tipousuario table
INSERT INTO tipousuario (nombre_tipo, estatus, usuario_registro, fecha_registro)
VALUES ('Administrador', 1, 1, NOW()),
       ('Usuario', 1, 1, NOW());

-- Inserts for menu table
INSERT INTO menu (nombre_menu, enlace, estatus, usuario_registro, fecha_registro)
VALUES ('Dashboard', '/dashboard', 1, 1, NOW()),
       ('Ventas', '/ventas', 1, 1, NOW()),
       ('Productos', '/productos', 1, 1, NOW());

-- Inserts for usuario table
INSERT INTO usuario (tipousuarioid_usua, nombrecompleto_usuario, fecha_nacimiento, estatus, usuario_registro, fecha_registro)
VALUES (1, 'Admin Admin', '1990-01-01', 1, 1, NOW()),
       (2, 'Usuario Normal', NULL, 1, 1, NOW());

-- Inserts for menu_tipousuario table
INSERT INTO menu_tipousuario (tipousuarioid_mt, menuid_mt, estatus)
VALUES (1, 1, 1),
       (1, 2, 1),
       (1, 3, 1),
       (2, 1, 1),
       (2, 2, 1),
       (2, 3, 1);

-- Inserts for cliente table
INSERT INTO cliente (antiguedad, nombre_cliente, correo, estatus, usuario_registro, fecha_registro)
VALUES (NOW(), 'Cliente 1', 'cliente1@example.com', 1, 'Admin', NOW()),
       (NOW(), 'Cliente 2', 'cliente2@example.com', 1, 'Admin', NOW());

-- Inserts for venta table
INSERT INTO venta (cliente_venta, usuario_venta, folio_venta, fecha_venta, cantidad_productos, total_ventas, estatus, fecha_registro)
VALUES (1, 1, 'FV20240001', '2024-03-24', 5, 100.50, 1, NOW()),
       (2, 1, 'FV20240002', '2024-03-24', 3, 75.25, 1, NOW());

-- Inserts for producto table
INSERT INTO producto (nombre_pd, alias, dias_caducidad, unidad_medida, costo_producto, estatus, usuario_registro, fecha_registro)
VALUES ('Producto 1', 'P1', 30, 'unidad', 10.50, 1, 1, NOW()),
       ('Producto 2', 'P2', 60, 'unidad', 20.75, 1, 1, NOW());

-- Inserts for ventaitem table
DESC ventaitem;
INSERT INTO ventaitem (ventaid_itm, paqueteid_itm, cantidad, subtotal, descuento, total, estatus, usuario_registro, fecha_registro)
VALUES (1, 1, 2, 21.00, 0, 21.00, 1, 1, NOW()),
       (1, 2, 3, 62.25, 0, 62.25, 1, 1, NOW()),
       (2, 1, 1, 10.50, 0, 10.50, 1, 1, NOW()),
       (2, 2, 2, 41.50, 0, 41.50, 1, 1, NOW());

-- Inserts for receta table
INSERT INTO receta (nombre_receta, alias, estatus, usuario_registro, fecha_registro)
VALUES ('Receta 1', 'R1', 1, 1, NOW()),
       ('Receta 2', 'R2', 1, 1, NOW());

-- Inserts for recetaitem table
INSERT INTO recetaitem (recetaid_itm, materialid_itm, cantidad_requerida, estatus, usuario_registro, fecha_registro)
VALUES (1, 1, 2.5, 1, 1, NOW()),
       (1, 2, 3.0, 1, 1, NOW()),
       (2, 1, 1.5, 1, 1, NOW()),
       (2, 2, 2.0, 1, 1, NOW());

-- Inserts for material table
INSERT INTO material (nombre_mat, dias_caducidad, unidad_medida, costo_mat, estatus, fecha_registro)
VALUES ('Material 1', NOW(), 'kg', 5.75, 1, NOW()),
       ('Material 2', NOW(), 'lt', 8.20, 1, NOW());

-- Inserts for proveedor table
INSERT INTO proveedor (nombre, telefono, correo, dias_visita, estatus, usuario_registro, fecha_registro)
VALUES ('Proveedor 1', '1234567890', 'prov1@example.com', 'Lunes', 1, 1, NOW()),
       ('Proveedor 2', '0987654321', 'prov2@example.com', 'Viernes', 1, 1, NOW());

-- Inserts for tipostock table
INSERT INTO tipostock (nombre_stock, estatus, usuario_registro, fecha_registro)
VALUES ('Tipo Stock 1', 1, 1, NOW()),
       ('Tipo Stock 2', 1, 1, NOW());

-- Inserts for tipoinventario table
INSERT INTO tipoinventario (nombre_tipoInv, estatus, usuarios_registro, fecha_registro)
VALUES ('Tipo Inventario 1', 1, 1, NOW()),
       ('Tipo Inventario 2', 1, 1, NOW());

-- Inserts for inventario table
INSERT INTO inventario (tipostock_inv, producto_inv, material_inv, tipo_inv, fecha_caducidad, proveedorid_inv, estatus, usuario_registro, fecha_registro)
VALUES (1, 1, 1, 1, '2024-12-31', 1, 1, 1, NOW()),
       (2, 2, 2, 2, '2024-06-30', 2, 1, 1, NOW());

-- Inserts for produccion table
INSERT INTO produccion (usuarioid_produce_prd, usuarioid_solicito_prd, folio_produccion, fecha_inicio, fecha_fin, cantidad_total, costo_total, estatus, fecha_registro)
VALUES 
    (1, 2, 'Prod20240001', NOW(), NULL, 50.0, 200.0, 1, NOW()), -- Inserting NULL into fecha_fin
    (1, 2, 'Prod20240002', NOW(), '2024-03-26', 75.0, 300.0, 1, NOW()); -- Inserting a different date into fecha_fin


-- Inserts for produccionitem table
INSERT INTO produccionitem (produccion_itm, producto_itm, cantidad, costo, estarus, usuario_registrado, fecha_registro)
VALUES (1, 1, 10, 40.0, 1, 1, NOW()),
       (1, 2, 15, 60.0, 1, 1, NOW()),
       (2, 1, 20, 80.0, 1, 1, NOW()),
       (2, 2, 30, 120.0, 1, 1, NOW());

-- Inserts for compra table
INSERT INTO compra (proveedorid_comp, usuario_comp, folio_comp, fecha_comp, cantidad, total, estaus, fecha_registro)
VALUES (1, 1, 'Comp20240001', NOW(), 100, 500.0, 1, NOW()),
       (2, 1, 'Comp20240002', NOW(), 150, 750.0, 1, NOW());

-- Inserts for compraitem table
INSERT INTO compraitem (compra_itm, materialid_itm, cantidad, subtotal, descuento, total, estatus, usuario_registro, fecha_registro)
VALUES (1, 1, 50, 287.50, 0, 287.50, 1, 1, NOW()),
       (1, 2, 50, 410.0, 0, 410.0, 1, 1, NOW()),
       (2, 1, 75, 431.25, 0, 431.25, 1, 1, NOW()),
       (2, 2, 75, 615.0, 0, 615.0, 1, 1, NOW());
