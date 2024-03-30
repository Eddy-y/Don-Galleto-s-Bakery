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
from flask_login import LoginManager,login_user,logout_user,login_required


from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
app.secret_key='esta es la clave secreta'

# Inicializa la extensión Admin
admin = Admin(app, name='MiAppAdmin', template_mode='bootstrap3', url='/panel_admin')
# Añade vistas al panel administrativo
admin.add_view(ModelView(Usuario, db.session))

login_manager_app=LoginManager(app)

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


@app.errorhandler(401)
def bad_request(e):
    return render_template('401.html'), 400

@login_manager_app.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
    
#Función del Login
@app.route('/', methods=["GET", "POST"])
def index():
    username=''
    password=''
    user_form = forms.UsersForm(request.form)
    if request.method == 'POST' and user_form.validate_on_submit():
        username = user_form.username.data
        password = user_form.password.data

        user = Usuario.query.filter_by(user=username).first()

        if user and check_password_hash(user.password,password):
            print('Exito')
            login_user(user)
            return redirect(url_for('pagePrincipal'))
        else:
            flash('Usuario o contraseña Incorrectos ...')
            print('No funciono')
        
    return render_template("index.html", form=user_form)

@app.route("/pagePrincipal")
def pagePrincipal():
    return render_template('layout.html')

#Función del Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

#Funcion que permite hacer el CRUD de los usuarios
@app.route("/pagePrincipal/user", methods=["GET", "POST"])
@login_required
def user():
    user_formreg = forms.UserFormReg(request.form)
    allUsuarios=Usuario.query.all()
    if request.method == 'POST':
        action = request.form.get('action')
        #Reguistro de Usuarios
        if request.form.get('registrar') and user_formreg.validate_on_submit():
            try:
                newUser=Usuario(tipousuario=user_formreg.tipousuario.data,
                            nombrecompleto=user_formreg.nombrecompleto.data,
                            usuario_registro=request.form.get('idUser'),
                            user = user_formreg.username.data,
                            password = generate_password_hash(user_formreg.password.data)
                            )
                db.session.add(newUser)
                db.session.commit()
                flash('Usuario Registrado Correctamente...')
                user_formreg.nombrecompleto.data=''
                user_formreg.username.data=''
                user_formreg.password.data=''
            except Exception as e:
                db.session.rollback()
                print(f"Error al agregar el usuario: {e}")
        #Eliminar Usuarios
        elif action == 'eliminar':
            id=request.form.get('idUserDelete')
            print(id)
            user_to_delete=Usuario.query.get(id)
            if user_to_delete:
                user_to_delete.estatus=False
                print(user_to_delete.estatus)
                db.session.commit()
                
            else:
                print('Error')
        #Editar Usuarios
        elif action == 'editarS':
            id=request.form.get('idUserEdit')
            print(id)
            existing_user=Usuario.query.get(id)
            
            if existing_user:
                existing_user.nombrecompleto=user_formreg.nombrecompleto.data
                existing_user.tipousuario = user_formreg.tipousuario.data
                existing_user.username = user_formreg.username.data
                
                if user_formreg.password.data:
                    existing_user.password = generate_password_hash(user_formreg.password.data)
                
                existing_user.ultima_modificacion = datetime.now()
                
                db.session.commit()
                flash('Usuario Editado Correctamente...')
                #Se limpia el formulario
                user_formreg.nombrecompleto.data=''
                user_formreg.username.data=''
                user_formreg.password.data=''
            else:
                print('Fallo la modificacion')
            
            
    return render_template('modules/usuarios.html', form=user_formreg,users=allUsuarios)

#Función del CRUD de Proveedores
@app.route("/pagePrincipal/proveedor", methods=["GET", "POST"])
@login_required
def proveedor():
    #user_formreg = forms.UserFormReg(request.form)
    #allUsuarios=Usuario.query.all()
    if request.method == 'POST':
        print('Hola')
    
    return render_template('modules/proveedores.html')


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()