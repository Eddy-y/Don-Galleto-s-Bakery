use cookiesInc;
SET sql_safe_updates = 0;


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
/*INSERT INTO produccion (folio_produccion, fecha_inicio, cantidad_total, costo_total, estatus, fecha_registro, fecha_fin)
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
(8, 8, 5, 50, 'Activo', 1, NOW(), 8); */

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
       (2, 1, 'FV20240002', '2024-03-24', 3, 75.25, 1, NOW()),
       (2, 1, 'FV20240003', '2024-03-24', 2, 10, 1, NOW()),
       (1, 1, 'FV20240004', '2024-03-24', 10, 100, 1, NOW());

       
INSERT INTO ventaitem (ventaid_itm, paqueteid_itm, cantidad, subtotal, descuento, total, estatus, usuario_registro, fecha_registro)
VALUES (1, 1, 2, 21.00, 0, 21.00, 1, 1, NOW()),
       (1, 2, 3, 62.25, 0, 62.25, 1, 1, NOW()),
       (2, 1, 1, 10.50, 0, 10.50, 1, 1, NOW()),
       (2, 2, 2, 41.50, 0, 41.50, 1, 1, NOW()),
       (3, 3, 1, 10.50, 0, 10.50, 1, 1, NOW()),
       (3, 3, 1, 10.50, 0, 10.50, 1, 1, NOW());
       
UPDATE inventario
SET material_inv = null -- Calcula el material_inv basado en el rango de id_inventario
WHERE id_inventario BETWEEN 23 AND 27;

-- Delete not useful records
delete from inventario where producto_inv in (1,2);
delete from inventario where id_inventario in (23,24,26);

-- AGREGAR CONECCION ENTRE PRODUCCION Y PRODUCCIONITEM
ALTER TABLE produccion
ADD COLUMN id_produccionitem INT,
ADD CONSTRAINT fk_produccionitem FOREIGN KEY (id_produccionitem) REFERENCES produccionitem(id_produccionitem);

-- DROPEAR REGISTROS INUTILES
/*SET FOREIGN_KEY_CHECKS = 0;
DELETE FROM produccion;
SET FOREIGN_KEY_CHECKS = 1;*/


-- PROCEDIMIENTO ALMACENADO PARA DESCONTAR MATERIALES
drop procedure if exists descontarProduccion;
DELIMITER //
CREATE PROCEDURE descontarProduccion(
	IN var_idProducto int,
    IN var_cantidad int,
    IN var_idProduccionitem int
)
BEGIN
	declare costo double;
	DECLARE done INT DEFAULT FALSE;
    DECLARE idMaterial INT;
    DECLARE cantidadRestar INT;
	 -- Cursor para recorrer los resultados de la subconsulta
    DECLARE cur CURSOR FOR
        SELECT ri.materialid_itm AS idMat, SUM(ri.cantidad * var_cantidad) AS reCant
        FROM recetaitem ri
        WHERE ri.productoid_itm = var_idProducto
        GROUP BY ri.materialid_itm;
    -- Declaraciones para manejar errores
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    -- Abrir el cursor
    OPEN cur;
    read_loop: LOOP
        -- Leer los valores del cursor
        FETCH cur INTO idMaterial, cantidadRestar;
        IF done THEN
            LEAVE read_loop;
        END IF;
        -- Actualizar la tabla inventario restando el campo reCant de la consulta al registro con el campo idMat de la consulta
        UPDATE inventario
        SET cantidad_inv = cantidad_inv - cantidadRestar
        WHERE material_inv = idMaterial;
    END LOOP;
    -- Cerrar el cursor
    CLOSE cur;
    -- AGREGAR INVENTARIO CREADO
    UPDATE inventario
    SET cantidad_inv = cantidad_inv + var_cantidad
    WHERE producto_inv = var_idProducto;
    
    update produccionitem
    set cantidad = var_cantidad
    where id_produccionitem = var_idProduccionitem;
    
    select costo into costo from produccionitem where id_produccionitem = var_idProduccionitem;
    
    update produccion
    set cantidad_total = var_cantidad, fecha_fin = now(), costo_total = costo*var_cantidad
    where id_produccionitem = var_idProduccionitem;
END //
DELIMITER ;
        
call descontarProduccion(8,1,10);

-- PROCEDIMIENTO ALMACENADO PARA DESCONTAR MATERIALES
drop procedure if exists agregarProduccion;
DELIMITER //
CREATE PROCEDURE agregarProduccion(
	IN var_idProducto int
)
BEGIN
	DECLARE last_id INT;
	declare var_costo double;
    
	select sum(costo_mat) into var_costo from recetaitem ri
    join material m on m.id_material = ri.materialid_itm
    where ri.productoid_itm = var_idProducto
    group by ri.productoid_itm;
    
	INSERT INTO produccionitem (productoid_itm, costo, estatus, fecha_registro) VALUES (var_idProducto,var_costo,1,now());
    SELECT LAST_INSERT_ID() INTO last_id;
    
    insert into produccion(fecha_inicio,estatus,fecha_registro,id_produccionitem) values(now(),1,now(),last_id);
END //
DELIMITER ;

-- CONSULTA IMPORTANTE: PARA VER CUANTOS MATERIALES FALTAN PARA CADA RECETA (EJEMPLO 10)
select m.id_material, m.nombre_mat as material, inv.cantidad_inv as tenemos, ri.cantidad as necesarias
from produccionitem pi
JOIN produccion p ON p.id_produccionitem = pi.id_produccionitem
JOIN producto prod ON prod.id_producto = pi.productoid_itm
JOIN recetaitem ri ON ri.productoid_itm = prod.id_producto
JOIN material m ON m.id_material = ri.materialid_itm
join inventario inv on inv.material_inv = m.id_material
where pi.id_produccionitem = 10;
        