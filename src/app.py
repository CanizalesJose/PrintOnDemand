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
from modelos.userTypeDAO import userTypeDAO
from modelos.material import material
from modelos.materialDAO import materialDAO
from modelos.validMaterial import validMaterial
from modelos.validMaterialDAO import validMaterialDAO


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
        # request.for['username']: esta linea toma el valor del formulario con un atributo name = 'username'
        # el atributo id no es necesario para estas transacciones y solo se usará en el JS
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
                            <form id="catalogoForm{validModel[0]}">
                                Cantidad: <input type="number" class="cantidad" id="cantidadProducto{validModel[0]}" value="1">
                                </p>
                                <label>Seleccionar material: </label>
                                <select class="form-select" aria-label="Seleccion de material" id="tipoProducto{validModel[0]}">
                                    {materialsList}
                                </select>
                                <br>
                                <div class="text-center">
                                    <button type="button" class="btn btn-primary agregar" id="button{validModel[0]}">Agregar al carrito</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                
            """
    return render_template("auth/catalogo.html", catalogo=catalogo)

@app.route("/adminModels")
def adminModels():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        mensaje = request.args.get('mensaje', "")
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
                        <input type="hidden" name="modelId" value="{modelo.getModelId()}">
                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" name="inputUpdatedModelName{modelo.getModelId()}" value="{modelo.getModelName()}">
                            <label for="inputUpdatedModelName{modelo.getModelId()}">Nuevo nombre</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" name="inputUpdatedModelImage{modelo.getModelId()}" value="{modelo.getModelImage()}">
                            <label for="inputUpdatedModelName{modelo.getModelId()}">Nueva Imagen</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" name="inputUpdatedModelFile{modelo.getModelId()}" value="{modelo.getModelFile()}">
                            <label for="inputUpdatedModelFile{modelo.getModelId()}">Nuevo archivo</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="number" class="form-control" name="inputUpdatedModelBasePrice{modelo.getModelId()}" value="{modelo.getModelBasePrice()}">
                            <label for="inputUpdatedModelBasePrice{modelo.getModelId()}">Nuevo precio base</label>
                        </div>

                        <!-- <div class="form-floating mb-1">
                            <input type="file" class="form-control" id="inputUpdatedModelFile{modelo.getModelFile()}" value="{modelo.getModelFile()}">
                            <label for="inputUpdatedModelBasePrice{modelo.getModelId()}">Archivo del modelo:</label>
                        </div> -->

                        <button type="button" class="btn btn-primary bg-gradient mt-3" id="updateProduct{modelo.getModelId()}">Modificar</button>
                        <button type="button" class="btn btn-danger bg-gradient mt-3" id="deleteProduct{modelo.getModelId()}">Eliminar</button>
                    </form>
                </td>
            </tr>
            """
        return render_template("auth/adminModels.html", listaModelosHTML=listaModelosHTML, mensaje=mensaje)
    else:
        return redirect('catalogo')

@app.route("/adminUsers")
def adminUsers():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        # Genera los tipos de usuarios y los agrega a las opciones
        userTypesListHTML = ""
        userTypesList = userTypeDAO.getUserTypes(db)
        for registro in userTypesList:
            userTypesListHTML += f"""
                <option value="{registro.getUserTypeId()}">{registro.getUserTypeName()}</option>
            """
        # Generar la lista de usuarios registrados
        usersList = UserDAO.getFullUserData(db)
        userListHTML = ""
        for registro in usersList:
            userListHTML += f"""
            <tr>
                <td>{registro['usuario'].getUserName()}</td>
                <td>{registro['usertype'].getUserTypeId()}</td>
                <td>{registro['usertype'].getUserTypeName()}</td>
                <td>
                    <form id="updateUser{registro['usuario'].getUserName()}">
                        <input type="hidden" name="userName" value="{registro['usuario'].getUserName()}">
                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" id="inputUpdatedUsername{registro['usuario'].getUserName()}" value="{registro['usuario'].getUserName()}">
                            <label for="inputUpdatedUsername{registro['usuario'].getUserName()}">Nuevo nombre</label>
                        </div>

                        <label >Tipo de usuario</label
                        <br><br>
                        <select class="form-select" aria-label="Seleccion de tipo" id="inputUpdatedUserType{registro['usuario'].getUserName()}">
                            {userTypesListHTML}
                        </select>


                        <button type="button" class="btn btn-primary bg-gradient mt-3" id="updateUser{registro['usuario'].getUserName()}">Modificar</button>
                        <button type="button" class="btn btn-danger bg-gradient mt-3" id="deleteUser{registro['usuario'].getUserName()}">Eliminar</button>
                    </form>
                </td>
            </tr>
            """
        
        return render_template("auth/adminUsers.html", userTypesListHTML=userTypesListHTML, userListHTML=userListHTML)
    else:
        return redirect('catalogo')

@app.route("/adminMaterials")
def adminMaterials():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        mensaje = request.args.get('mensaje', "")
        materialsList = materialDAO.getAllMaterials(db)
        materialsListHTML = ""
        for material in materialsList:
            materialsListHTML += f"""
            <tr>
                <td scope="col">{material.getMaterialId()}</td>
                <td scope="col">{material.getMaterialName()}</td>
                <td scope="col">x {material.getMaterialPriceModifier()}</td>
                <td scope="col">
                    <form id="updateFormMaterial{material.getMaterialId()}">
                        <input type="hidden" name="materialId" value="{material.getMaterialId()}">
                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" id="inputUpdatedMaterialName{material.getMaterialId()}" value="{material.getMaterialName()}">
                            <label for="inputUpdatedMaterialName{material.getMaterialId()}">Nuevo Nombre</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="number" class="form-control" id="inputUpdatedMaterialPriceModifier{material.getMaterialId()}" value="{material.getMaterialPriceModifier()}">
                            <label for="inputUpdatedMaterialPriceModifier{material.getMaterialId()}">Multiplicador de precio</label>
                        </div>

                        <button type="button" class="btn btn-primary bg-gradient mt-3" id="updateMaterial{material.getMaterialId()}">Modificar</button>
                        <button type="button" class="btn btn-danger bg-gradient mt-3" id="deleteMaterial{material.getMaterialId()}">Eliminar</button>
                    </form>
                </td>
            </tr>
            """
        return render_template("auth/adminMaterials.html", materialsListHTML=materialsListHTML, mensaje=mensaje)
    else:
        return redirect('catalogo')

@app.route("/adminValidMaterials")
def adminValidMaterials():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        mensaje = request.args.get('mensaje', "")
        # Generar lista de modelos validos
        validModels = validMaterialDAO.getModelsIdWithMaterials(db)
        validModelsOptionsHTML = ""
        if validModels != None:
            for modelo in validModels:
                validModelsOptionsHTML += f"""
                    <option value="{modelo.getModelId()}">{modelo.getModelName()}</option>
                """
        # Generar la lista de materiales
        materialsList = materialDAO.getAllMaterials(db)
        if materialsList != None:
            materialsListHTML = ""
            for material in materialsList:
                materialsListHTML += f"""
                    <option value="{material.getMaterialId()}">{material.getMaterialName()}</option>
                """
        # Generar la tabla con los materiales de cada modelo
        validList = validMaterialDAO.getDataValidMaterials(db)
        
        if validList != None:
            validListHTML = ""
            for registro in validList:
                validListHTML += f"""
                    <tr>
                        <td>{registro['modelName']}</td>
                        <td>{registro["materialName"]}</td>
                        <td> <img src="{registro["modelImage"]}" class="imgMdl"></td>
                        <td>
                            <form>
                                <input type="hidden" name="modelKey" value="{registro['modelKey']}">
                                <input type="hidden" name="materialKey" value="{registro['materialKey']}">
                                <button type="button" class="btn btn-danger bg-gradient mt-3" id="deleteValidElement{registro['modelKey']+registro['materialKey']}">Eliminar</button>
                            </form>
                        </td>
                    </tr>
                """

        return render_template("auth/adminValidMaterials.html", validModelsOptionsHTML=validModelsOptionsHTML, materialsListHTML=materialsListHTML, validListHTML=validListHTML, mensaje=mensaje)
    else:
        return redirect('catalogo')

@app.route("/pedidos")
def pedidosPersonalizados():
    if current_user.is_authenticated:
        return render_template("auth/realizarPedidos.html")
    else:
        return redirect(url_for('catalogo'))
    
@app.route("/addModel", methods=["GET", "POST"])
def addModel():
    if request.method == "POST":
        # Gestionar el agregar modelo
        mensaje = ""
        newId = request.form['inputNewModelId']
        newName = request.form['inputNewModelName']
        newImage = request.form['inputNewModelImage']
        newFile = request.form['inputNewModelFile']
        newPrice = float(request.form['inputNewModelBasePrice'])

        modelo = Model3D(newId, newName, newImage, newFile, newPrice)
        if len(modelo.getModelId()) == 0:
            mensaje += "<div class=\"alert alert-danger\" role=\"alert\"> El campo id no puede estar vacío </div>"
        if len(modelo.getModelName()) == 0:
            mensaje += "<div class=\"alert alert-danger\" role=\"alert\"> El campo nombre no puede estar vacío </div>"
        if len(modelo.getModelImage()) == 0:
            mensaje += "<div class=\"alert alert-danger\" role=\"alert\"> El campo imagen no puede estar vacío </div>"
        if len(modelo.getModelFile()) == 0:
            mensaje += "<div class=\"alert alert-danger\" role=\"alert\"> El campo archivo no puede estar vacío </div>"
        if modelo.getModelBasePrice() <= 0:
            mensaje += "<div class=\"alert alert-danger\" role=\"alert\"> El campo precio no puede ser igual o menor a 0 </div>"
        
        if mensaje != "":
            return redirect(url_for("adminModels", mensaje=mensaje))
        
        if model3DDAO.insertModel3D(db, modelo) == 1:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\"> El id del modelo ya existe </div>"
        else:
            mensaje = "<div class=\"alert alert-success\" role=\"alert\"> Modelo agregado! </div>"

        return redirect(url_for("adminModels", mensaje=mensaje))

    else:
        mensaje = ""
        return redirect(url_for("adminModels", mensaje=mensaje))
    
@app.route("/addMaterial", methods=["GET", "POST"])
def addMaterial():
    if request.method == "POST":
        mensaje = ""
        newId = request.form['newMaterialId']
        newName = request.form['newMaterialName']
        newPriceModifier = float(request.form['newMaterialPriceModifier'])
        newMaterial = material(newId, newName, newPriceModifier)

        if len(newMaterial.getMaterialId()) == 0:
            mensaje += "<div class=\"alert alert-danger\" role=\"alert\"> El id no puede estar vacío </div>"
        if len(newMaterial.getMaterialName()) == 0:
            mensaje += "<div class=\"alert alert-danger\" role=\"alert\"> El nombre no puede estar vacío </div>"
        if float(newMaterial.getMaterialPriceModifier()) <= 0:
            mensaje += "<div class=\"alert alert-danger\" role=\"alert\"> El modificador de precio no puede ser 0 o menor </div>"

        if mensaje != "":
            return redirect(url_for("adminMaterials", mensaje=mensaje))
        if materialDAO.insertMaterial(db, newMaterial) == 1:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\"> El id del nuevo material ya existe </div>"
        else:
            mensaje = "<div class=\"alert alert-success\" role=\"alert\"> Material agregado! </div>"

        return redirect(url_for("adminMaterials", mensaje=mensaje))
    else:
        mensaje = ""
        return redirect(url_for("adminMaterials"), mensaje=mensaje)
    
@app.route("/addValidMaterial", methods=["GET", "POST"])
def addValidMaterials():
    if request.method == "POST":
        mensaje = ""
        newModelKey = request.form['inputValidModel']
        newMaterialKey = request.form['inputValidMaterial']
        vinculo = validMaterial(newModelKey, newMaterialKey)

        if validMaterialDAO.insertValidMaterial(db, vinculo) == 1:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\"> La relación ya existe </div>"
        else:
            mensaje = "<div class=\"alert alert-success\" role=\"alert\"> Relación agregada! </div>"
        return redirect(url_for("adminValidMaterials",mensaje=mensaje))
    else:
        mensaje = ""
        return redirect(url_for("adminValidMaterials", mensaje=mensaje))


# Definición de rutas predeterminadas
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def defaultRute(path):
#     return redirect(url_for("iniciarSesion"))


# Al ejecutar el archivo, inicia el servidor
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(use_reloader=True)