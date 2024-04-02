use cookiesInc;

show tables;
        

desc produccion;
desc produccionitem;
desc paqueteItem;


select * from produccion;
select * from receta;

select * from material;

desc inventario;
desc producto;
show tables;

select * from paquete;
select * from paqueteitem;
select * from ventaitem;
select * from venta;
select * from inventario;
select * from producto;
select * from recetaitem;
select * from material; -- del mat 5 necesito 360
    
    
select m.id_material, m.nombre_mat as material, inv.cantidad_inv as tenemos, ri.cantidad as necesarias
from produccionitem pi
JOIN produccion p ON p.id_produccionitem = pi.id_produccionitem
JOIN producto prod ON prod.id_producto = pi.productoid_itm
JOIN recetaitem ri ON ri.productoid_itm = prod.id_producto
JOIN material m ON m.id_material = ri.materialid_itm
join inventario inv on inv.material_inv = m.id_material
where pi.id_produccionitem = 10;

UPDATE inventario
set cantidad_inv = cantidad_inv + 2000
where material_inv = 6;

select * from material;
select * from inventario;
select * from produccion;
select * from produccionitem;
select * from producto;
select * from recetaitem;
    
SELECT prod.nombre_producto as nombre, pi.costo as costo, pi.costo as costo, p.fecha_inicio as fechaInicio, coalesce(p.fecha_fin, 'En espera') as fechaFin, 
    CASE 
        WHEN p.fecha_fin IS NULL THEN 0 
        ELSE 1 
    END AS estado_fecha
    FROM produccion p JOIN produccionitem pi ON p.id_produccionitem = pi.id_produccionitem
    join producto prod on prod.id_producto = pi.productoid_itm
    WHERE p.fecha_inicio IS NOT NULL order by  p.fecha_inicio asc limit 6;
    
    
	
    
    select inv.id_inventario as idInv, p.id_producto as idPro, p.nombre_producto as nombre, inv.cantidad_inv as cantidad
    from inventario inv join producto p on inv.producto_inv = p.id_producto where p.id_producto not in (select pi.productoid_itm from produccionitem pi join produccion p ON p.id_produccionitem = pi.id_produccionitem where p.fecha_fin is null);
    
    select pi.productoid_itm from produccionitem pi join produccion p ON p.id_produccionitem = pi.id_produccionitem where p.fecha_fin is null;
	
    
    
    SELECT sum(ventaitem.cantidad) as cantidad, month(ventaitem.fecha_registro) as mes
        FROM ventaitem
        GROUP BY month(ventaitem.fecha_registro);
    
SELECT paquete.nombre_paq as nombre, sum(ventaitem.cantidad) as cantidad, month(ventaitem.fecha_registro) as mes 
	    FROM ventaitem
        JOIN venta ON venta.id_venta = ventaitem.ventaid_itm
        join paquete on ventaitem.paqueteid_itm = paquete.id_paquete
        GROUP BY venta.fecha_venta, paquete.nombre_paq;
    
    
    
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE
    TABLE_NAME = 'produccion';
