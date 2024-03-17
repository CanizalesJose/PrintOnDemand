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
                    <form action="/updateModel" method="POST">
                        <input type="hidden" name="modelId" value="{modelo.getModelId()}">
                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" name="updatedModelName" value="{modelo.getModelName()}">
                            <label for="updatedModelName">Nuevo nombre</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" name="updatedModelImage" value="{modelo.getModelImage()}">
                            <label for="updatedModelName">Nueva Imagen</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" name="updatedModelFile" value="{modelo.getModelFile()}">
                            <label for="updatedModelFile">Nuevo archivo</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="number" step="0.01" class="form-control" name="updatedModelBasePrice" value="{modelo.getModelBasePrice()}">
                            <label for="updatedModelBasePrice">Nuevo precio base</label>
                        </div>

                        <button type="submit" class="btn btn-primary bg-gradient mt-3" onclick="return confirm('¿Estás seguro de modificar este modelo?')">Modificar</button>
                    </form>

                    <form action="/deleteModel" method="POST">
                        <input type="hidden" name="modelId" value="{modelo.getModelId()}">
                        <button type="submit" class="btn btn-danger bg-gradient mt-3" onclick="return confirm('¿Estás seguro de eliminar este modelo? Se eliminaran todos las relaciones con materiales asignadas')">Eliminar</button>
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
        mensaje = request.args.get('mensaje', "")
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
                    <form action="/updateUser" method="POST">
                        <input type="hidden" name="currentUserName" value="{registro['usuario'].getUserName()}">

                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" name="newUsername" value="{registro['usuario'].getUserName()}">
                            <label for="newUsername">Nuevo nombre</label>
                        </div>
                        
                        <div class="form-floating mb-1">
                            <select class="form-select" aria-label="Seleccion de tipo" name="newUserType" placeholder="newUserType">
                                {userTypesListHTML}
                            </select>
                            <label for="newUserType">Tipo de usuario</label>
                        </div>

                        <button type="submit" class="btn btn-primary bg-gradient mt-3" onclick="return confirm('¿Estas seguro de modificar este usuario?')">Modificar</button>
                    </form>

                    <form action="/deleteUser" method="POST">
                        <input type="hidden" name="currentUserName" value="{registro['usuario'].getUserName()}">
                        <button type="submit" class="btn btn-danger bg-gradient mt-3" id="deleteUser{registro['usuario'].getUserName()}" onclick="return confirm('¿Estas seguro de eliminar este usuario?')">Eliminar</button>
                    </form>
                </td>
            </tr>
            """
        
        return render_template("auth/adminUsers.html", userTypesListHTML=userTypesListHTML, userListHTML=userListHTML, mensaje=mensaje)
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
                    <form action="/updateMaterial" method="POST">
                        <input type="hidden" name="materialId" value="{material.getMaterialId()}">
                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" placeholder="newMaterialName" name="newMaterialName" value="{material.getMaterialName()}">
                            <label for="newMaterialName">Nuevo Nombre</label>
                        </div>

                        <div class="form-floating mb-1">
                            <input type="number" step="0.01" class="form-control" name="newMaterialPriceModifier" placeholder="price" value="{material.getMaterialPriceModifier()}">
                            <label for="newMaterialPriceModifier">Multiplicador de precio</label>
                        </div>

                        <button type="submit" class="btn btn-primary bg-gradient mt-3" onclick="return confirm('¿Estás seguro de modificar este material?')">Modificar</button>
                    </form>
                    <form action="/deleteMaterial" method="POST">
                        <input type="hidden" name="materialId" value="{material.getMaterialId()}">
                        <button type="submit" class="btn btn-danger bg-gradient mt-3" onclick="return confirm('¿Estás seguro de eliminar este material? Se eliminarán las relaciones con modelos asignadas')">Eliminar</button>
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
        validModels = model3DDAO.getAllModels(db)
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
                            <form action="/deleteValidMaterial" method="POST">
                                <input type="hidden" name="modelKey" value="{registro['modelKey']}">
                                <input type="hidden" name="materialKey" value="{registro['materialKey']}">
                                <button type="submit" class="btn btn-danger bg-gradient mt-3" onclick="return confirm('¿Estás seguro de eliminar este material del modelo?')">Eliminar</button>
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


# ----------------------------------------------------------------------------------------------------
# Comienzan los métodos POST, para administrar los registros

# Modelos
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

@app.route("/updateModel", methods=["POST", "GET"])
def updateModel():
    if request.method == "POST":
        mensaje = ""
        modelId = request.form['modelId']
        modelName = request.form['updatedModelName']
        modelImage = request.form['updatedModelImage']
        modelFile = request.form['updatedModelFile']
        modelBasePrice = float(request.form['updatedModelBasePrice'])
        updatedModel = Model3D(modelId, modelName, modelImage, modelFile, modelBasePrice)

        if len(updatedModel.getModelId()) == 0 or len(updatedModel.getModelName()) == 0 or len(updatedModel.getModelImage()) == 0 or len(updatedModel.getModelFile()) == 0 or float(updatedModel.getModelBasePrice()) <= 0 or model3DDAO.updateModel3D(db, updatedModel) == 1:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema con los datos... </div>"
            return redirect(url_for("adminModels", mensaje=mensaje))
        else:
            mensaje = f"<div class=\"alert alert-success\" role=\"alert\"> Modelo \"{updatedModel.getModelId()}\" actualizado!</div>"
            return redirect(url_for("adminModels", mensaje=mensaje))
    else:
        mensaje = ""
        return redirect(url_for("adminModels", mensaje=mensaje))

@app.route("/deleteModel", methods=["POST", "GET"])
def deleteModel():
    if request.method == "POST":
        mensaje = ""
        modelId = request.form['modelId']

        if model3DDAO.deleteModel3D(db, modelId) == 1:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema inesperado... </div>"
            return redirect(url_for("adminModels", mensaje=mensaje))

        else:
            mensaje = f"<div class=\"alert alert-success\" role=\"alert\"> Modelo \"{modelId}\" eliminado!</div>"
            return redirect(url_for("adminModels", mensaje=mensaje))
    else:
        mensaje = ""
        return redirect(url_for("adminModels", mensaje=mensaje))
    

# Materiales
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
    
@app.route("/updateMaterial", methods=["GET", "POST"])
def updateMaterial():
    if request.method == "POST":
        mensaje = ""
        currentId = request.form['materialId']
        newName = request.form['newMaterialName']
        newPriceMod = request.form['newMaterialPriceModifier']

        updatedMaterial = material(currentId, newName, float(newPriceMod))

        if len(updatedMaterial.getMaterialName()) == 0 or updatedMaterial.getMaterialPriceModifier() <= 0 or materialDAO.updateMaterial(db, updatedMaterial) == 1:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema al actualizar... </div>"
        else:
            mensaje = "<div class=\"alert alert-success\" role=\"alert\"> Material actualizado! </div>"

        return redirect(url_for("adminMaterials", mensaje=mensaje))
    else:
        mensaje = ""
        return redirect(url_for("adminMaterials", mensaje=mensaje))

@app.route("/deleteMaterial", methods=["GET", "POST"])
def deleteMaterial():
    if request.method == "POST":
        mensaje = ""
        materialId = request.form['materialId']

        newMaterial = material(materialId, "", "")
        try:
            if materialDAO.deleteMaterial(db, newMaterial.getMaterialId()) == 1:
                mensaje = "<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema al eliminar... </div>"
            else:
                mensaje = "<div class=\"alert alert-success\" role=\"alert\"> Material eliminado! </div>"
        except Exception as ex:
            mensaje =  "<div class=\"alert alert-success\" role=\"alert\">" + str(Exception(ex)) + "</div>"
        return redirect(url_for("adminMaterials", mensaje=mensaje))
    else:
        mensaje = ""
        return redirect(url_for("adminMaterials", mensaje=mensaje))

# Materiales Validos
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

@app.route("/deleteValidMaterial", methods=["GET", "POST"])
def deleteValidMaterial():
    if request.method == "POST":
        mensaje = ""
        modelKey = request.form['modelKey']
        materialKey = request.form['materialKey']
        eliminado = validMaterial(modelKey, materialKey)
        try:
            if validMaterialDAO.deleteValidMaterial(db,eliminado) == 1:
                mensaje = "<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema al eliminar... </div>"
            else:
                mensaje = "<div class=\"alert alert-success\" role=\"alert\"> Relación eliminada! </div>"
        except Exception as ex:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\">" + str(Exception(ex)) + "</div>"
        return redirect(url_for("adminValidMaterials", mensaje=mensaje))
    else:
        mensaje = ""
        return redirect(url_for("adminValidMaterials", mensaje=mensaje))
    
# Usuarios
@app.route("/addUser", methods=["GET", "POST"])
def addUser():
    if request.method == "POST":
        mensaje = ""
        newUsername = request.form['inputNewUserName']
        newUsertype = int(request.form['inputNewUserType'])
        newPassword = request.form['inputNewUserPassword']
        newUser = user(newUsername, newUsertype, newPassword)
        try:
            if len(newUser.getUserName()) == 0 or len(newUser.getUserName()) > 100:
                mensaje += "<div class=\"alert alert-danger\" role=\"alert\"> El nombre debe ser tener entre 1 y 100 caracteres </div>"
            if len(newUser.getUserPassword()) == 0:
                mensaje += "<div class=\"alert alert-danger\" role=\"alert\"> La contraseña no puede estar vacía </div>"
            if UserDAO.addUser(db, newUser) == 1:
                mensaje = "<div class=\"alert alert-danger\" role=\"alert\"> El usuario ya existe </div>"
            else:
                mensaje = "<div class=\"alert alert-success\" role=\"alert\"> Usuario agregado! </div>"
            
        except Exception as ex:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\">" + str(Exception(ex)) + "</div>"
        
        return redirect(url_for("adminUsers", mensaje=mensaje))
    else:
        mensaje = ""
        return redirect(url_for("adminUsers", mensaje=mensaje))

@app.route("/updateUser", methods=["GET", "POST"])
def updateUser():
    if request.method == "POST":
        mensaje = ""
        currentUsername = request.form['currentUserName']
        newUsername = request.form['newUsername']
        newUserType = int(request.form['newUserType'])

        try:
            if len(newUsername) == 0:
                mensaje = "<div class=\"alert alert-danger\" role=\"alert\"> El nombre no puede estar vacío </div>"
            
            if current_user.getUserName() == currentUsername:
                mensaje = "<div class=\"alert alert-danger\" role=\"alert\">" + "No puedes modificar al usuario activo" + "</div>"
                return redirect(url_for("adminUsers", mensaje=mensaje))
            resultado = UserDAO.updateUser(db, currentUsername, newUsername, newUserType)

            if resultado == 1:
                mensaje = "<div class=\"alert alert-danger\" role=\"alert\">" + "El usuario no existe" + "</div>"
            if resultado == 2:
                mensaje = "<div class=\"alert alert-danger\" role=\"alert\">" + "El nuevo nombre de usuario ya existe" + "</div>"
            if resultado == 0:
                mensaje = "<div class=\"alert alert-success\" role=\"alert\">" + "Usuario modificado" + "</div>"
        except Exception as ex:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\">" + str(Exception(ex)) + "</div>"
        return redirect(url_for("adminUsers", mensaje=mensaje))
    else:
        mensaje = ""
        return redirect(url_for("adminUsers", mensaje=mensaje))
    
@app.route("/deleteUser", methods=["GET", "POST"])
def deleteUser():
    if request.method == "POST":
        mensaje = ""
        deletedUsername = request.form['currentUserName']
        if current_user.getUserName() == deletedUsername:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\">" + "No puedes eliminar al usuario activo" + "</div>"
            return redirect(url_for("adminUsers", mensaje=mensaje))
        
        try:
            if UserDAO.deleteUser(db, deletedUsername) == 1:
                mensaje = "<div class=\"alert alert-danger\" role=\"alert\">" + "El usuario no existe" + "</div>"
            else:
                mensaje = "<div class=\"alert alert-success\" role=\"alert\">" + "Usuario eliminado" + "</div>"
        except Exception as ex:
            mensaje = "<div class=\"alert alert-danger\" role=\"alert\">" + str(Exception(ex)) + "</div>"
        return redirect(url_for("adminUsers", mensaje=mensaje))
    else:
        mensaje = ""
        return redirect(url_for("adminUsers", mensaje=mensaje))

# En caso de ingresar una ruta que no existe
@app.errorhandler(404)
def rutaInexistente(e):
    return redirect(url_for('iniciarSesion'))


# Al ejecutar el archivo, inicia el servidor
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(use_reloader=True)