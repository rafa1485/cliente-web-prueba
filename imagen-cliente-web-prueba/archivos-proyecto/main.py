from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Configuración inicial
app = Flask(__name__)
app.secret_key = b'elsecretodetusojos'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige a /login si no está autenticado

# Lista de usuarios (usuario, clave) en formato (nombre, contraseña_hash)
usuarios = [
    ("admin", generate_password_hash("admin123")),
    ("user1", generate_password_hash("pass1")),
    ("user2", generate_password_hash("pass2")),
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
                return redirect(url_for("home"))

        flash("Usuario o contraseña incorrectos", "danger")

    return render_template("login.html")

# Ruta para cerrar sesión
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for("login"))

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
