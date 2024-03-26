from flask import Flask, render_template, request, jsonify, flash, redirect, session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask
from flask_cors import CORS, cross_origin
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import forms
from datetime import datetime
from models import Usuario
from models import db


from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
app.secret_key='esta es la clave secreta'

# Inicializa la extensión Admin
admin = Admin(app, name='MiAppAdmin', template_mode='bootstrap3', url='/panel_admin')

# Añade vistas al panel administrativo
admin.add_view(ModelView(Usuario, db.session))

#BLOQUEAR TODOS LOS ORIGENES
#CORS(app, resources={r"/*": {"origins": ""}})

#DESBLOQUEAR TODOS LOS ORIGENES
#CORS(app, resources={r"/*": {"origins": "*"}})

# DESBLOQUEAR CIERTOS ORIGENES
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5000"]}})
#CORS(app, resources={r"/*": {"origins": ["http://192.168.111.246.*", "http://192.168.111.86:8080","http://192.168.111.127.*"]}})

#--------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

@app.route('/', methods=["GET", "POST"])
def index():
    user_form = forms.UsersForm(request.form)
    if request.method == 'POST':
        username = user_form.username.data
        password = user_form.password.data

        user = Usuario.query.filter_by(user=username).first()

        if (user.user == username) and (user.password == password):
            print('Exito')
            return 'Inicio de sesión exitoso!'
        else:
            print('No funciono')
            return 'Credenciales inválidas!'
        
        
        
    return render_template("index.html", form=user_form)




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/principal')
@login_required
def principal():        
    #Agregar mensajes a la lista de flash
    mensaje='Bienvenido a la app'
    flash(mensaje)
    return render_template('principal.html')



def log_login_attempt(username, success, error_message):
    try:
        cur = mysql.connection.cursor()
        # Llamada al procedimiento almacenado en lugar de la consulta directa
        cur.callproc('InsertarLoginLog', (username, success, error_message))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print("Error occurred while logging login attempt:", str(e))

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()