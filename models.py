from flask_sqlalchemy import SQLAlchemy
import datetime


db=SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    tipousuarioid_usua = db.Column(db.String(50), nullable=False)
    nombrecompleto_usuario = db.Column(db.String(70), nullable=False)
    estatus = db.Column(db.Boolean, default=True)  # BIT en MySQL se maneja como Boolean en SQLAlchemy
    usuario_registro = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    
