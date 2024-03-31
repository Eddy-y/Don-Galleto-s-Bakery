from wtforms import Form, StringField, PasswordField, validators

class UsersForm(Form):
    username = StringField('Username', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=10, message='Ingresa un usuario válido')
    ])
    password = PasswordField('Password', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=10, message='Ingresa una contraseña válida'),
        validators.Regexp(
            regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
            message='Contraseña: contener al menos una mayúscula, minúscula, un número y un carácter especial'
        ),
        validators.EqualTo('confirm_password', message='Las contraseñas deben coincidir')
    ])
    confirm_password = PasswordField('Confirm Password', [
        validators.DataRequired(message='El campo es requerido jjjddd')
    ])

    
