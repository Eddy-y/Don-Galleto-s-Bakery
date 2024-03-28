use cookiesInc;

show tables;
        
select month('2024-03-24 21:33:23');
select * from venta;
select * from ventaitem;
SELECT count(*) FROM producto where dias_caducidad < 20;
SELECT count(*) as cantidadVentas, sum(total_ventas) as total FROM venta;

SELECT p.folio_produccion as folio, pi.cantidad as cantidad, pi.costo as costo, paq.nombre_paq as nombrePaquete, paq.costopaquete_paq as costoPaquete, p.fecha_inicio as fechaInicio
    FROM produccion p JOIN produccionitem pi ON p.id_produccion = pi.produccion_itm JOIN paqueteitem paqIt ON paqIt.id_paqueteitem = pi.id_paqueteitem join paquete paq on paqIt.paqueteid_itm = paq.id_paquete
    WHERE p.fecha_fin IS NULL AND p.fecha_inicio IS NOT NULL;
    
SELECT p.folio_produccion as folio, p.cantidad_total as cantidad, p.costo_total as costo FROM produccion p
    WHERE p.fecha_fin IS NULL AND p.fecha_inicio IS NOT NULL;

desc produccion;
desc produccionitem;
desc paqueteItem;


select * from produccion;
select * from receta;
select * from inventario;
select * from material;

desc inventario;
show tables;

SELECT p.nombre_paq AS productoVendido, COUNT(vi.id_ventaitem) AS cantidad_ventas 
    FROM ventaitem vi 
    JOIN paqueteitem pi ON vi.paqueteid_itm = pi.id_paqueteitem
    join paquete p on p.id_paquete = pi.paqueteid_itm
    GROUP BY p.nombre_paq
    ORDER BY cantidad_ventas DESC LIMIT 1; 


SELECT COUNT(*) AS cuenta 
FROM inventario 
WHERE DATEDIFF(fecha_caducidad, CURDATE()) <= 20;

