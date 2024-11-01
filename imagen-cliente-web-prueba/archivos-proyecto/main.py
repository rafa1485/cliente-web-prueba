from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ingredientes import conectar, tabla_existe, crear_tabla, inicializar_tabla_ingredientes, agregar_ingrediente, obtener_ingrediente, modificar_ingrediente, borrar_ingrediente

conectar()

existencia_tabla_ingredientes = tabla_existe('ingredientes')
if not existencia_tabla_ingredientes:
    crear_tabla()
    inicializar_tabla_ingredientes()

# Configuración inicial
app = Flask(__name__)
app.secret_key = b'elsecretodetusojos'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige a /login si no está autenticado

# Lista de usuarios (usuario, clave) en formato (nombre, contraseña_hash)
usuarios = [
    ("admin", generate_password_hash("admin123")),
    ("edgar", generate_password_hash("ceape2024")),
    ("user", generate_password_hash("test2024")),
]

# Clase de usuario que extiende UserMixin para integración con Flask-Login
class Usuario(UserMixin):
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

# Cargar usuario por ID (Flask-Login necesita esta función)
@login_manager.user_loader
def load_user(user_id):
    for i, (nombre, _) in enumerate(usuarios):
        if str(i) == user_id:
            return Usuario(i, nombre)
    return None

# Ruta protegida que solo puede accederse si el usuario está autenticado
@app.route("/")
@login_required
def home():
    #flash("Bienvenido, se ha logeado correctamente", "message")
    return f"<h1>Bienvenido, {current_user.nombre}!</h1><a href='/logout'>Cerrar sesión</a>"

# Ruta para iniciar sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Validar credenciales contra la lista de usuarios
        for i, (nombre, clave_hash) in enumerate(usuarios):
            if nombre == username and check_password_hash(clave_hash, password):
                user = Usuario(i, nombre)
                login_user(user)
                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for('seleccion_app'))

        flash("Usuario o contraseña incorrectos", "danger")

    return render_template("login.html")

# Ruta para cerrar sesión
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for("login"))


# Seleccionar app
@app.route('/seleccion_app')
@login_required
def seleccion_app():
    return render_template('select_apps.html')


##*****************************************************************************************
# Ruta principal que muestra todos los ingredientes
@app.route('/abm_ingredientes')
@login_required
def abm_ingredientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ingredientes")
    ingredientes = cursor.fetchall()
    conexion.close()
    return render_template('ingredientes.html', ingredientes=ingredientes)

# Ruta para agregar un nuevo ingrediente
@app.route('/abm_ingredientes/agregar', methods=['POST'])
@login_required
def agregar():
    nombre = request.form['nombre']
    densidad = request.form['densidad']
    precio = request.form['precio']
    color = request.form['color']
    contenido_proteico = request.form['contenido_proteico']
    contenido_carbohidratos = request.form['contenido_carbohidratos']
    contenido_aceites = request.form['contenido_aceites']
    histidina = request.form['histidina']
    isoleucina = request.form['isoleucina']
    leucina = request.form['leucina']
    lisina = request.form['lisina']
    metionina = request.form['metionina']
    fenilalanina = request.form['fenilalanina']
    treonina = request.form['treonina']
    triptofano = request.form['triptofano']
    valina = request.form['valina']
    
    agregar_ingrediente(nombre, float(densidad), float(precio), color, float(contenido_proteico),
                                     float(contenido_carbohidratos), float(contenido_aceites), float(histidina),
                                     float(isoleucina), float(leucina), float(lisina), float(metionina),
                                     float(fenilalanina), float(treonina), float(triptofano), float(valina))
    return redirect(url_for('abm_ingredientes'))

# Ruta para eliminar un ingrediente
@app.route('/abm_ingredientes/eliminar/<int:id>')
@login_required
def eliminar(id):
    borrar_ingrediente(id)
    return redirect(url_for('abm_ingredientes'))

# Ruta para editar un ingrediente
@app.route('/abm_ingredientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if request.method == 'POST':
        densidad = request.form['densidad']
        precio = request.form['precio']
        color = request.form['color']
        contenido_proteico = request.form['contenido_proteico']
        contenido_carbohidratos = request.form['contenido_carbohidratos']
        contenido_aceites = request.form['contenido_aceites']
        histidina = request.form['histidina']
        isoleucina = request.form['isoleucina']
        leucina = request.form['leucina']
        lisina = request.form['lisina']
        metionina = request.form['metionina']
        fenilalanina = request.form['fenilalanina']
        treonina = request.form['treonina']
        triptofano = request.form['triptofano']
        valina = request.form['valina']

        modificar_ingrediente(id, float(densidad), float(precio), color, float(contenido_proteico),
                                           float(contenido_carbohidratos), float(contenido_aceites), float(histidina),
                                           float(isoleucina), float(leucina), float(lisina), float(metionina),
                                           float(fenilalanina), float(treonina), float(triptofano), float(valina))
        return redirect(url_for('abm_ingredientes'))
    else:
        ingrediente = obtener_ingrediente(id)
        return render_template('ingredientes.html', editar=True, ingrediente=ingrediente)


##*************************************************************************************************************

# Aplicacion de mezcla óptima

# Ruta para seleccionar ingredientes y calcular los valores
@app.route('/mezcla_manual', methods=['GET', 'POST'])
@login_required
def mezcla_manual():
    ingredientes = []
    score_proteico = 0
    costo_por_kg = 0
    porcentaje_total = 0

    if request.method == 'POST':
        # Cargar datos de la selección y porcentajes
        seleccionados = request.form.getlist('ingrediente')
        porcentajes = request.form.getlist('porcentaje')
        
        for i, ingrediente_id in enumerate(seleccionados):
            porcentaje = float(porcentajes[i]) if porcentajes[i] else 0
            ingrediente = obtener_ingrediente(ingrediente_id)
            
            if ingrediente:
                nombre, precio, contenido_proteico = ingrediente[1], ingrediente[3], ingrediente[5]
                ingredientes.append({
                    'nombre': nombre,
                    'porcentaje': porcentaje,
                    'precio': precio,
                    'contenido_proteico': contenido_proteico
                })
                
                # Cálculos de porcentaje total, score proteico y costo por kg
                porcentaje_total += porcentaje
                score_proteico += (contenido_proteico * porcentaje / 100)
                costo_por_kg += (precio * porcentaje / 100)

    else:
        # Muestra todos los ingredientes para seleccionar
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM ingredientes")
        ingredientes = cursor.fetchall()
        conexion.close()

    return render_template('mezcla_manual.html', ingredientes=ingredientes, 
                           score_proteico=score_proteico, costo_por_kg=costo_por_kg, 
                           porcentaje_total=porcentaje_total)

# Aplicacion de mezcla óptima
@app.route('/mezcla_optima')
@login_required
def mezcla_optima():
    return f'''
               <h1>Bienvenido a la prueba de Mezcla Óptima, {current_user.nombre}!</h1>
               <a href='/logout'>Cerrar sesión</a>
            '''




# Punto de entrada de la aplicación
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
