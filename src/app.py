# Importar librerias
from flask import Flask, render_template, redirect, request, url_for, flash, get_flashed_messages, abort, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from config.config import config
import json
from modelos.model3D import Model3D
from modelos.model3DDAO import model3DDAO
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

# Definición de rutas para páginas

@app.route("/logout")
def logout():
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
            mensaje = """
            <div class="alert alert-danger" role="alert">
                Usuario o contraseña incorrectos...
            </div>
            """
            return render_template('auth/InicioSesion.html', mensaje=mensaje)
    else:
        if current_user.is_authenticated:
            return redirect(url_for('catalogo'))
        return render_template('auth/InicioSesion.html')

@app.route("/catalogo")
def catalogo():

    catalogo = ""
    # Recorre cada modelo
    for elemento in model3DDAO.showAllModelId(db):
        # Conseguir los id de los modelos que se van a mostrar, los que tienen materiales asignados
        validModel = model3DDAO.getValidModel(db, elemento)
        if validModel != None:
            # Conseguir los materiales del modelo
            materials = model3DDAO.getMaterialsFromModel(db, elemento)
            materialsList = ""
            for material in materials:
                materialsList = materialsList + f"""
                <option value="{material["materialId"]}">{material["materialName"]} ($ * {material["materialPriceModifier"]})</option>
                """

            catalogo = catalogo + f"""
             <div class="col-md-3 my-4">
                    <div class="card text-dark rounded">
                        <img src="{validModel[2]}" class="card-img-top imgArticulo" alt="Producto {validModel[0]}">
                        <div class="card-body">
                            <h5 class="card-title">{validModel[1]}</h5>
                            <p class="card-text">${validModel[4]}
                            <br>
                            Cantidad: <input type="number" class="cantidad" id="cantidadProducto{validModel[0]}" value="1">
                            </p>
                            <br>
                            <select class="form-select" aria-label="Default select example">
                                {materialsList}
                            </select>
                            <br>
                            <div class="text-center">
                                <button type="button" class="btn btn-primary agregar" id="button{validModel[0]}">Agregar al carrito</button>
                            </div>
                        </div>
                    </div>
                </div>
                
            """
    return render_template("auth/catalogo.html", catalogo=catalogo)

@app.route("/pedidos")
def pedidosPersonalizados():
    return render_template("plantillaBase.html")

@app.route("/adminModels")
def adminModels():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        listaModelosHTML = ""
        listaModelos = model3DDAO.getAllModels(db)

        for modelo in listaModelos:
            listaModelosHTML += f"""
            <tr>
                <td>{modelo.getModelId()}</td>
                <td>{modelo.getModelName()}</td>
                <td><img src="{modelo.getModelImage()}" class="imgMdl"></td>
                <td>{modelo.getModelFile()}</td>
                <td>{modelo.getModelBasePrice()}</td>
                <td>
                    <form id="updateForm{modelo.getModelId()}">
                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" id="inputUpdatedModelName{modelo.getModelId()}" value="{modelo.getModelName()}">
                            <label for="inputUpdatedModelName{modelo.getModelId()}">Nuevo nombre</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" id="inputUpdatedModelImage{modelo.getModelId()}" value="{modelo.getModelImage()}">
                            <label for="inputUpdatedModelName{modelo.getModelId()}">Nueva Imagen</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" id="inputUpdatedModelFile{modelo.getModelId()}" value="{modelo.getModelFile()}">
                            <label for="inputUpdatedModelFile{modelo.getModelId()}">Nuevo archivo</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="number" class="form-control" id="inputUpdatedModelBasePrice{modelo.getModelId()}" value="{modelo.getModelBasePrice()}">
                            <label for="inputUpdatedModelBasePrice{modelo.getModelId()}">Nuevo precio base</label>
                        </div>

                        <button type="button" class="btn btn-primary bg-gradient mt-3" id="updateProduct{modelo.getModelId()}">Modificar</button>
                        <button type="button" class="btn btn-danger bg-gradient mt-3" id="deleteProduct{modelo.getModelId()}">Eliminar</button>
                    </form>
                </td>
            </tr>
            """
        return render_template("auth/adminModels.html", listaModelosHTML=listaModelosHTML)
    else:
        return redirect('catalogo')


# Definición de rutas predeterminadas
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def defaultRute(path):
#     return redirect(url_for("iniciarSesion"))


# Al ejecutar el archivo, inicia el servidor
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(use_reloader=True)