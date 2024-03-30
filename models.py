from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_login import UserMixin


db=SQLAlchemy()

class Usuario(db.Model,UserMixin):
    __tablename__ = 'usuario'

    id_us = db.Column(db.Integer, primary_key=True)  # Auto increment se maneja automáticamente
    tipousuario = db.Column(db.String(50), nullable=False)
    nombrecompleto = db.Column(db.String(70), nullable=False)
    estatus = db.Column(db.String(1), default='1')  # BIT en MySQL se maneja como Boolean en SQLAlchemy
    usuario_registro = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ultima_sesion = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ultima_modificacion = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def get_id(self):
        return str(self.id_us)
    
