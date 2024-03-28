from flask import Flask, render_template, request, jsonify, flash, redirect, session,url_for
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_cors import CORS, cross_origin
from functools import wraps
from flask_wtf.csrf import CSRFProtect
import forms
from datetime import datetime

from config import DevelopmentConfig

 
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
#BLOQUEAR TODOS LOS ORIGENES
#CORS(app, resources={r"/*": {"origins": ""}})

#DESBLOQUEAR TODOS LOS ORIGENES
#CORS(app, resources={r"/*": {"origins": "*"}})

# DESBLOQUEAR CIERTOS ORIGENES
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5000"]}})
#CORS(app, resources={r"/*": {"origins": ["http://192.168.111.246.*", "http://192.168.111.86:8080","http://192.168.111.127.*"]}})

mysql = MySQL(app)

#--------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('Manejadores/404.html'),404
@app.errorhandler(400)
def bad_request(e):
    return render_template('Manejadores/400.html'), 400

@app.route('/',methods=["GET","POST"])
def index():
    username=''
    password=''
    msg=''
    cur=''
    user_form = forms.UsersForm(request.form)

    if request.method == 'POST' and user_form.validate():
        username = user_form.username.data
        password = user_form.password.data
        # print(generate_password_hash('V1ct0rG@y', "scrypt", 16))

        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM GetAllUsuarios WHERE admin_name = %s", [username])
            user_data = cur.fetchone()
            

            if user_data:
                if user_data['account_locked']:
                    # Verifica si ha pasado el tiempo de bloqueo
                    lock_time = user_data['lock_time']
                    if lock_time is not None and (datetime.now() - lock_time).total_seconds() < DevelopmentConfig.TIME_TO_UNLOCK:
                        # Si la cuenta está bloqueada pero el tiempo de bloqueo no ha pasado, muestra un mensaje de cuenta bloqueada temporalmente
                        msg = 'Your account is temporarily locked. Please try again later.'
                        print('segundos transcurridos', (datetime.now() - lock_time).total_seconds())
                        print(msg)
                        return render_template("index.html", form=user_form, msg=msg)
                    else:
                         # Si ha pasado el tiempo de bloqueo, desbloquea la cuenta usando el procedimiento almacenado
                        cur.callproc('ToggleUserLock', (username, False))
                        mysql.connection.commit()
                db_password = user_data['admin_password']
                failed_attempts = user_data['failed_login_attempt']

                if failed_attempts >= DevelopmentConfig.MAX_FAILED_ATTEMPTS:
                    # Bloquea la cuenta si ha excedido el número máximo de intentos fallidos
                    cur.callproc('ToggleUserLock', (username, True))
                    mysql.connection.commit()
                    msg = 'Too many failed login attempts. Please try again later.'
                elif check_password_hash(db_password, password):
                    session['logged_in'] = True
                    session['username'] = username
                    # Llamar al procedimiento almacenado para actualizar los intentos fallidos
                    cur.execute("CALL UpdateFailedLoginAttempts(%s, %s)", (username, 0))
                    mysql.connection.commit()
                    # Registro de log de inicio de sesión exitoso
                    log_login_attempt(username, True, None)
                    msg="success"
                    return redirect('principal')
                else:
                    msg = 'Invalid credentials'
                    # Incrementar el contador de intentos fallidos
                    cur.execute("CALL UpdateFailedLoginAttempts(%s, %s)", (username, failed_attempts + 1))
                    mysql.connection.commit()
                    log_login_attempt(username, False, msg)
            else:
                msg = 'User not found'
                log_login_attempt(username, False, msg)

        except Exception as e:
            # Manejar errores de base de datos de manera adecuada
            #msg = 'Error occurred: {}'.format(str(e))
            msg = 'Usuario sin intentos por la siguiente hora, intente mas tarde.'
            # Registro de log de inicio de sesión fallido
            log_login_attempt(username, False, str(e))
        finally:
            # Cerrar el cursor después de haber trabajado con los datos
            if cur:
                cur.close()
        return render_template("index.html",form=user_form, msg=msg)
    return render_template("index.html",form=user_form)

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        data = request.get_json()  # Get JSON data from the request
        if 'username' in data and 'password' in data:
            username = data['username']
            password = data['password']

            try:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT * FROM usuario WHERE admin_name = %s", [username])
                user_data = cur.fetchone()
                cur.close()

                if user_data:
                    db_password = user_data['admin_password']
                    if check_password_hash(db_password, password):
                        session['logged_in'] = True
                        session['username'] = username
                        msg = 'success'
                    else:
                        msg = 'Invalid credentials'
                else:
                    msg = 'User not found'

            except Exception as e:
                # Manejar errores de base de datos de manera adecuada
                msg = 'Error occurred: {}'.format(str(e))
        else:
            msg = 'Missing username or password in the request'

    else:
        msg = 'Invalid request method'

    return jsonify({'msg': msg})

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

# ''''''''''''''''''''''''''DASHBOARD'''''''''''''''''''''''''''''''''''''''
@app.route('/dashboard')
def dashboard():    
    ventas = getVentasAnio()
    produccion = getProduccion()
    caducidadesINV = getCaducidades()
    cardData = getCards()

    print(cardData)

    for item in cardData:
        caducidades = item['Caducidades']
        cantidadVentas = item['cantidadVentas']
        totalVentas = item['totalVentas']
        productoVendido = item['productoVendido']

    return render_template("Dashboard/dashboard.html",produccion=produccion, ventas = ventas, caducidadesINV=caducidadesINV,productoVendido=productoVendido, caducidades=caducidades, cantidadVentas = cantidadVentas, totalVentas=totalVentas)

@app.route('/get_ventasPr', methods=['GET'])
def get_ventasPr():
    # Get the week number from the request parameters
    week_number = request.args.get('week_number')
    # print(week_number)

    # Prepare the SQL query to filter by week and sum quantities
    query = """
        SELECT paquete.nombre_paq as nombre, sum(ventaitem.cantidad) as cantidad, month(ventaitem.fecha_registro) as mes 
	    FROM ventaitem
        JOIN venta ON venta.id_venta = ventaitem.ventaid_itm
        JOIN paqueteitem ON ventaitem.paqueteid_itm = paqueteitem.id_paqueteitem
        join paquete on paqueteitem.paqueteid_itm = paquete.id_paquete
        WHERE month(ventaitem.fecha_registro) = %s
        GROUP BY venta.fecha_venta, paquete.nombre_paq;
    """

    # Execute the query with the week number parameter
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query, (week_number,))
    data = cur.fetchall()
    cur.close()
    # print(data)

    return jsonify(data)

@app.route('/getVentasAnio', methods=['GET'])
def getVentasAnio():
    query = """
        SELECT sum(ventaitem.cantidad) as cantidad, month(ventaitem.fecha_registro) as mes
        FROM ventaitem
        GROUP BY month(ventaitem.fecha_registro);
    """
    # Ejecutar la consulta
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    # print(data)

    return jsonify(data)

def getVentasAnio():
    query = """
        SELECT cliente_venta AS Cliente_ID,
            folio_venta AS Folio_Venta,
            fecha_venta AS Fecha_Venta,
            id_venta AS Id_Venta,
            total_ventas AS Total_Venta
        FROM venta
        ORDER BY fecha_registro DESC
        LIMIT 9;
    """
    # Ejecutar la consulta
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    # print(data)
    return data

def getCaducidades():
    query = """
    SELECT 
    inv.fecha_caducidad AS caducidadInventario,
    COALESCE(p.nombre_receta, m.nombre_mat) AS nombre,
    inv.id_inventario AS idInventario
    FROM 
    inventario inv 
    JOIN 
    material m ON inv.material_inv = m.id_material 
    JOIN 
    receta p ON inv.producto_inv = p.id_receta
    ORDER BY inv.fecha_caducidad ASC;
    """
    # Ejecutar la consulta
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    # print(data)
    return data

def getCards():
    data = []

    query = """ SELECT COUNT(*) AS cuenta FROM inventario WHERE DATEDIFF(fecha_caducidad, CURDATE()) <= 20;"""
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    caducidades = cur.fetchone()

    query = """ SELECT count(*) as cantidadVentas FROM venta; """
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    cantidadVentas = cur.fetchone()

    query = """ SELECT sum(total_ventas) as totalVentas FROM venta; """
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    totalVentas = cur.fetchone()
    cur.close()

    query = """SELECT p.nombre_paq AS productoVendido, COUNT(vi.id_ventaitem) AS cantidad_ventas 
    FROM ventaitem vi 
    JOIN paqueteitem pi ON vi.paqueteid_itm = pi.id_paqueteitem
    join paquete p on p.id_paquete = pi.paqueteid_itm
    GROUP BY p.nombre_paq
    ORDER BY cantidad_ventas DESC LIMIT 1; """
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    productoVendido = cur.fetchone()
    cur.close()

    # Append the results to the data list
    data.append({
        "Caducidades": caducidades['cuenta'],
        "cantidadVentas": cantidadVentas['cantidadVentas'],
        "totalVentas": totalVentas['totalVentas'],
        "productoVendido": productoVendido['productoVendido']

    })

    return data

def getProduccion():
    query = """  SELECT p.folio_produccion as folio, pi.cantidad as cantidad, pi.costo as costo, paq.nombre_paq as nombrePaquete, paq.costopaquete_paq as costoPaquete, p.fecha_inicio as fechaInicio
    FROM produccion p JOIN produccionitem pi ON p.id_produccion = pi.produccion_itm JOIN paqueteitem paqIt ON paqIt.id_paqueteitem = pi.id_paqueteitem join paquete paq on paqIt.paqueteid_itm = paq.id_paquete
    WHERE p.fecha_fin IS NULL AND p.fecha_inicio IS NOT NULL;"""
    # Ejecutar la consulta
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    # print(data)
    return data
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# ''''''''''''''''''''''''''PRODUCCION'''''''''''''''''''''''''''''''''''''''
@app.route('/produccion')
def produccion():

    


    return render_template("Produccion/produccion.html")

@app.route('/produccionGalleta')
def produccionGalleta():
    return render_template("Produccion/producirGalleta.html")

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

if __name__ == "__main__":
    csrf.init_app(app)
    app.run(port=DevelopmentConfig.port, host='0.0.0.0')