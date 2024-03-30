from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators,ValidationError,IntegerField,DateTimeLocalField,SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional,Regexp
import re

def no_sql_injection(form, field):
    sql_patterns = [
        r';',           
        r'--',          
        r'union\s',    
        r'select\s',  
        r'insert\s',  
        r'delete\s',  
        r'update\s',
        r'drop\s',  
        r'exec\s', 
        r'xp_',
    ]
    for pattern in sql_patterns:
        if re.search(pattern, field.data, re.IGNORECASE):
            raise ValidationError('Entrada inválida detectada.')
class UsersForm(FlaskForm):
    username = StringField('Usuario', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=25, message='Ingresa un usuario válido'),
        no_sql_injection
    ])
    password = PasswordField('Contraseña', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=12, message='Ingresa una contraseña válida'),
        no_sql_injection
    ])

class UserFormReg(FlaskForm):
    id_us = IntegerField('ID')
    tipousuario = SelectField('Tipo de Usuario', 
                            choices=[('operProduccion','Operador de producción'),('ejecVentas','Operador punto de venta'),('adminInventario','Administrador de Inventario')],
                            validators=[DataRequired(message='El tipo de usuario es requerido')])
    nombrecompleto = StringField('Nombre Completo',[validators.DataRequired(message='El campo es requerido')])
    estatus = IntegerField('Estatus') 
    usuario_registro = IntegerField('Usuario Registro')
    fecha_registro = DateTimeLocalField('Fecha de Registro')
    ultima_sesion = DateTimeLocalField('Última Sesión')
    ultima_modificacion = DateTimeLocalField('Última Modificación')
    username = StringField('Usuario',[validators.DataRequired(message='El usuario es requerido'),
                                        validators.Length(min=4, max=50, message='El usuario debe tener entre 4 y 50 caracteres')]
                            )
    password = PasswordField('Contraseña',
                                validators=[
            DataRequired(message='La contraseña es requerida'),
            Length(min=6, message='La contraseña debe tener al menos 6 caracteres'),
            Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$',
            message='La contraseña debe incluir al menos una mayúscula, una minúscula, un número y un carácter especial.'
        )
        ])