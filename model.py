from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

db=SQLAlchemy()

class TipoUsuario(db.Model):
    id_tipousuario = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(50), nullable=False)
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False)

class Menu(db.Model):
    id_menu = db.Column(db.Integer, primary_key=True)
    nombre_menu = db.Column(db.String(50), nullable=False)
    enlace = db.Column(db.String(200))
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False)

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    tipousuarioid_usua = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id_tipousuario'), nullable=False)
    nombrecompleto_usuario = db.Column(db.String(70), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime)
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False)

class MenuTipoUsuario(db.Model):
    tipousuarioid_mt = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id_tipousuario'), primary_key=True, nullable=False)
    menuid_mt = db.Column(db.Integer, db.ForeignKey('menu.id_menu'), primary_key=True, nullable=False)
    estatus = db.Column(db.Boolean, nullable=False, default=True)

class Cliente(db.Model):
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    antiguedad = db.Column(db.DateTime)
    nombre_cliente = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.String(50))
    fecha_registro = db.Column(db.DateTime)

class Venta(db.Model):
    id_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_venta = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'))
    usuario_venta = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    folio_venta = db.Column(db.String(50))
    fecha_venta = db.Column(db.Date)
    fecha_cancelacion = db.Column(db.Date)
    cantidad_productos = db.Column(db.Integer)
    total_ventas = db.Column(db.Float)
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    fecha_registro = db.Column(db.DateTime)

class Producto(db.Model):
    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_pd = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50))
    dias_caducidad = db.Column(db.Integer)
    unidad_medida = db.Column(db.String(10))
    costo_producto = db.Column(db.Float)
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False)

class VentaItem(db.Model):
    id_ventaitem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venta_itm = db.Column(db.Integer, db.ForeignKey('venta.id_venta'))
    producto_itm = db.Column(db.Integer, db.ForeignKey('producto.id_producto'))
    cantidad = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
    descuento = db.Column(db.Float)
    total = db.Column(db.Float)
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime)

class ProductoMaterial(db.Model):
    id_receta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_receta = db.Column(db.String(50))
    alias = db.Column(db.String(50))
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime)

class Material(db.Model):
    id_material = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_mat = db.Column(db.String(15))
    dias_caducidad = db.Column(db.DateTime)
    unidad_medida = db.Column(db.String(50))
    costo_mat = db.Column(db.Float)
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    fecha_registro = db.Column(db.DateTime)

class Proveedor(db.Model):
    id_proveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(20))
    dias_visita = db.Column(db.String(50))
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime)

class Tipostock(db.Model):
    id_tipostock = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_stock = db.Column(db.String(50))
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime)

class Tipoinventario(db.Model):
    id_tipoInventario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_tipoInv = db.Column(db.String(50))
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuarios_registro = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime)

class Inventario(db.Model):
    id_inventario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipostock_inv = db.Column(db.Integer, db.ForeignKey('tipostock.id_tipostock'))
    producto_inv = db.Column(db.Integer, db.ForeignKey('producto.id_producto'))
    material_inv = db.Column(db.Integer, db.ForeignKey('material.id_material'))
    tipo_inv = db.Column(db.Integer, db.ForeignKey('tipoinventario.id_tipoInventario'))
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime)

class Produccion(db.Model):
    id_produccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    folio_produccion = db.Column(db.String(50))
    fecha_inicio = db.Column(db.DateTime)
    cantidad_total = db.Column(db.Float)
    costo_total = db.Column(db.Float)
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    fecha_registro = db.Column(db.DateTime)

class ProduccionItem(db.Model):
    id_produccionitem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produccion_itm = db.Column(db.Integer, db.ForeignKey('produccion.id_produccion'))
    material_itm = db.Column(db.Integer, db.ForeignKey('material.id_material'))
    cantidad = db.Column(db.Integer)
    costo = db.Column(db.Float)
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registrado = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime)

class Compra(db.Model):
    id_compra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proveedorid_comp = db.Column(db.Integer, db.ForeignKey('proveedor.id_proveedor'))
    usuario_comp = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    folio_comp = db.Column(db.String(50))
    fecha_comp = db.Column(db.DateTime)
    fecha_cancelacion = db.Column(db.DateTime)
    cantidad = db.Column(db.Integer)
    total = db.Column(db.Float)
    estaus = db.Column(db.Boolean, nullable=False, default=True)
    fecha_registro = db.Column(db.DateTime)

class CompraItem(db.Model):
    id_compraitem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    compra_itm = db.Column(db.Integer, db.ForeignKey('compra.id_compra'))
    materialid_itm = db.Column(db.Integer, db.ForeignKey('material.id_material'))
    cantidad = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
    descuento = db.Column(db.Float)
    total = db.Column(db.Float)
    estatus = db.Column(db.Boolean, nullable=False, default=True)
    usuario_registro = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime)