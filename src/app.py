# Importar librerias
from flask import Flask, render_template, redirect, request, url_for, flash, get_flashed_messages, abort, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from config.config import config
import json
from modelos.model3D import Model3D
from modelos.user import user
from modelos.UserDAO import UserDAO


# Crear instancias
app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(userName):
    return UserDAO.get_by_name(db, str(userName))

# Decorador para verificar si un usuario es admin
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.usertype != 1:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view


# Definición de rutas predeterminadas
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def defaultRute(path):
    return redirect(url_for("iniciarSesion"))

# Definición de rutas para páginas

@app.route("/logout")
def logout():
    print("se hace un logout")
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("iniciarSesion"))


@app.route("/inicio", methods = ["GET", "POST"])
def iniciarSesion():
    if request.method == "POST":
        usuario = user(request.form['username'], 0, request.form['password'])
        logged_user = UserDAO.login(db, usuario)

        if logged_user != None:
            login_user(logged_user)
            return redirect(url_for('catalogo'))
        else:
            return redirect(url_for('iniciarSesion'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('catalogo'))
        return render_template('auth/InicioSesion.html')

@app.route("/catalogo")
@login_required
def catalogo():
    if current_user.is_authenticated:
        print("esta autenticado")
        usuarioRegistrado = "en efecto, se autenticó"
        return render_template("auth/catalogo.html", usuarioRegistrado=usuarioRegistrado)
    else:
        print("no esta autenticado")
        return render_template("auth/catalogo.html")

@app.route("/pedidos")
def pedidosPersonalizados():
    return render_template("plantillaBase.html")


# Al ejecutar el archivo, inicia el servidor
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(use_reloader=False)