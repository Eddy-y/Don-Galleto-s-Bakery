use cookiesInc;

desc paqueteitem;

-- AGREGAR FOREIGN KEY DE paqueteitem a produccionitem
ALTER TABLE produccionItem
ADD COLUMN id_paqueteitem INT; -- Cambia el tipo de datos según sea necesario

ALTER TABLE produccionitem
ADD CONSTRAINT fk_paqueteitem_id
FOREIGN KEY (id_paqueteitem) 
REFERENCES paqueteitem(id_paqueteitem);
-- -----------------------------------------------------
-- AGREGAR campo fechaFin
ALTER TABLE produccion
ADD COLUMN fecha_fin DATETIME;


-- INSERTS DE PRODUCCION
INSERT INTO produccion (folio_produccion, fecha_inicio, cantidad_total, costo_total, estatus, fecha_registro, fecha_fin)
VALUES 
('PROD-001', '2024-03-27', 10, 100, 'Activo', NOW(), null),
('PROD-002', '2024-03-28', 15, 150, 'Activo', NOW(), '2024-04-06'),
('PROD-003', '2024-03-29', 20, 200, 'Activo', NOW(), null),
('PROD-004', '2024-03-30', 25, 250, 'Activo', NOW(), '2024-04-08'),
('PROD-005', '2024-03-31', 30, 300, 'Activo', NOW(), null),
('PROD-006', '2024-04-01', 35, 350, 'Activo', NOW(), '2024-04-10'),
('PROD-007', '2024-04-02', 40, 400, 'Activo', NOW(), '2024-04-11'),
('PROD-008', '2024-04-03', 45, 450, 'Activo', NOW(), null);

-- INSERTS DE PRODUCCIONITEM
INSERT INTO produccionitem (produccion_itm, productoid_itm, cantidad, costo, estatus, usuario_registrado, fecha_registro, id_paqueteitem)
VALUES 
(1, 1, 5, 50, 'Activo', 1, NOW(), 1),
(2, 2, 5, 50, 'Activo', 1, NOW(), 2),
(3, 3, 5, 50, 'Activo', 1, NOW(), 3),
(4, 4, 5, 50, 'Activo', 1, NOW(), 4),
(5, 5, 5, 50, 'Activo', 1, NOW(), 5),
(6, 6, 5, 50, 'Activo', 1, NOW(), 6),
(7, 7, 5, 50, 'Activo', 1, NOW(), 7),
(8, 8, 5, 50, 'Activo', 1, NOW(), 8);

-- update a registros de inventario
UPDATE inventario
SET material_inv = (id_inventario - 19) -- Calcula el material_inv basado en el rango de id_inventario
WHERE id_inventario BETWEEN 23 AND 27;

UPDATE inventario
SET producto_inv = 1 -- Calcula el material_inv basado en el rango de id_inventario
WHERE id_inventario BETWEEN 23 AND 25;

UPDATE inventario
SET producto_inv = 2 -- Calcula el material_inv basado en el rango de id_inventario
WHERE id_inventario BETWEEN 26 AND 27;

-- INSERT DE VENTAS
INSERT INTO venta (cliente_venta, usuario_venta, folio_venta, fecha_venta, cantidad_productos, total_ventas, estatus, fecha_registro)
VALUES (1, 1, 'FV20240001', '2024-03-24', 5, 100.50, 1, NOW()),
       (2, 1, 'FV20240002', '2024-03-24', 3, 75.25, 1, NOW());
       
INSERT INTO ventaitem (ventaid_itm, paqueteid_itm, cantidad, subtotal, descuento, total, estatus, usuario_registro, fecha_registro)
VALUES (1, 1, 2, 21.00, 0, 21.00, 1, 1, NOW()),
       (1, 2, 3, 62.25, 0, 62.25, 1, 1, NOW()),
       (2, 1, 1, 10.50, 0, 10.50, 1, 1, NOW()),
       (2, 2, 2, 41.50, 0, 41.50, 1, 1, NOW());