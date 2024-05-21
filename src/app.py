#region Importar librerías
from flask import Flask, render_template, redirect, request, url_for, flash, abort, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, current_user
from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import threading
from functools import wraps
from config.config import config
import random
from suds.client import Client
import json
from auxMethods.auxMethods import auxMethods
from modelos.model3D import Model3D
from modelos.model3DDAO import model3DDAO
from modelos.user import user
from modelos.UserDAO import UserDAO
from modelos.userTypeDAO import userTypeDAO
from modelos.material import material
from modelos.materialDAO import materialDAO
from modelos.validMaterial import validMaterial
from modelos.validMaterialDAO import validMaterialDAO
from modelos.orderModel import orderModel
from modelos.orderModelDAO import orderModelDAO
from modelos.orderDAO import orderDAO
from modelos.UserService import UserService
#endregion

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

@app.route("/logout", methods=["GET"])
def logout():
    if current_user.is_authenticated:
        logout_user()
    session.clear()
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
            flash('<div class="alert alert-danger" role="alert">Usuario o contraseña incorrectos...</div>')
            return render_template('auth/InicioSesion.html')
    else:
        if current_user.is_authenticated:
            return redirect(url_for('catalogo'))
        return render_template('auth/InicioSesion.html')

@app.route("/catalogo", methods=["GET"])
def catalogo():

    catalogo = auxMethods.generateCatalog(db)

    return render_template("auth/catalogo.html", catalogo=catalogo)

@app.route("/adminModels", methods=["GET"])
def adminModels():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        listaModelosHTML = auxMethods.generateModelList(db)
        
        return render_template("auth/adminModels.html", listaModelosHTML=listaModelosHTML)
    else:
        return redirect('catalogo')

@app.route("/adminUsers", methods=["GET"])
def adminUsers():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        # Genera los tipos de usuarios y los agrega a las opciones
        lists = auxMethods.generateUserLists(db)
        userTypesListHTML = lists[0]
        userListHTML = lists[1]
        
        return render_template("auth/adminUsers.html", userTypesListHTML=userTypesListHTML, userListHTML=userListHTML)
    else:
        return redirect('catalogo')

@app.route("/adminMaterials", methods=["GET"])
def adminMaterials():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        materialsListHTML = auxMethods.generateMaterialsList(db)

        return render_template("auth/adminMaterials.html", materialsListHTML=materialsListHTML)
    else:
        return redirect('catalogo')

@app.route("/adminValidMaterials", methods=["GET"])
def adminValidMaterials():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        lists = auxMethods.generateValidMaterialsLists(db)
        validModelsOptionsHTML = lists[0]
        materialsListHTML = lists[1]
        validListHTML = lists[2]

        return render_template("auth/adminValidMaterials.html", validModelsOptionsHTML=validModelsOptionsHTML, materialsListHTML=materialsListHTML, validListHTML=validListHTML)
    else:
        return redirect('catalogo')

@app.route("/pedidosPersonalizados", methods=["GET"])
def pedidosPersonalizados():
    
    # Recuperar el carrito o crearlo
    username = ""
    if current_user.is_authenticated:
        username = current_user.getUserName()
    if f'carrito{username}' not in session:
        session[f'carrito{username}'] = []
    carrito = session[f'carrito{username}']

    lists = auxMethods.generateCustomOrders(db, carrito, current_user)

    materialsListHTML = lists[0]
    listaResumenHTML = lists[1]
    totalResumen = lists[2]
    orderListHTML= lists[3]
        
    return render_template("auth/realizarPedidos.html", materialsListHTML=materialsListHTML, listaResumenHTML=listaResumenHTML, totalResumen=totalResumen, orderListHTML=orderListHTML)


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# Comienzan los métodos POST, para administrar los registros

# Modelos
@app.route("/addModel", methods=["GET", "POST"])
def addModel():
    if request.method == "POST":
        # Gestionar el agregar modelo
        newId = request.form['inputNewModelId']
        newName = request.form['inputNewModelName']
        newImage = request.form['inputNewModelImage']
        newFile = request.form['inputNewModelFile']
        newPrice = float(request.form['inputNewModelBasePrice'])

        modelo = Model3D(newId, newName, newImage, newFile, newPrice)
        regresar = 0
        if len(modelo.getModelId()) == 0:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El campo id no puede estar vacío </div>")
            regresar = 1
        if len(modelo.getModelName()) == 0:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El campo nombre no puede estar vacío </div>")
            regresar = 1
        if len(modelo.getModelImage()) == 0:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El campo imagen no puede estar vacío </div>")
            regresar = 1
        if len(modelo.getModelFile()) == 0:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El campo archivo no puede estar vacío </div>")
            regresar = 1
        if modelo.getModelBasePrice() <= 0:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El campo precio no puede ser igual o menor a 0 </div>")
            regresar = 1
        
        if regresar != 0:
            return redirect(url_for("adminModels"))
        
        if model3DDAO.insertModel3D(db, modelo) == 1:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El id del modelo ya existe </div>")
        else:
            flash("<div class=\"alert alert-success\" role=\"alert\"> Modelo agregado! </div>")

        return redirect(url_for("adminModels"))

    else:
        return redirect(url_for("adminModels"))

# ---------------------------------------------------------------------------------------
# Ejemplo de Arquitectura REST
# Se usa el método HTTP PATCH para acceder a esta dirección, se maneja mediante ajax en JavaScripts (src/templates/auth/adminModels.html)
# Se actualiza el recurso de modelo parcialmente desde la base de datos
@app.route("/updateModel", methods=["PATCH", "GET"])
def updateModel():
    if request.method == "PATCH":
        # Recibir la información desde la petición ajax
        data = json.loads(request.get_data())
        # Separar los datos específicos de la información recuperada
        modelId = data['modelId']
        modelName = data['updatedModelName']
        modelImage = data['updatedModelImage']
        modelFile = data['updatedModelFile']
        modelBasePrice = float(data['updatedModelBasePrice'])
        updatedModel = Model3D(modelId, modelName, modelImage, modelFile, modelBasePrice)

        # Si los campos no cumplen con los requisitos, rechaza la petición
        # Se manda a llamar la función a la base de datos, si es rechazada, también se cancelan los mensajes
        if len(updatedModel.getModelId()) == 0 or len(updatedModel.getModelName()) == 0 or len(updatedModel.getModelImage()) == 0 or len(updatedModel.getModelFile()) == 0 or float(updatedModel.getModelBasePrice()) <= 0 or model3DDAO.updateModel3D(db, updatedModel) == 1:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema con los datos... </div>")
            # return redirect(url_for("adminModels"))
            return "1"
        else:
            # Si los campos
            flash(f"<div class=\"alert alert-success\" role=\"alert\"> Modelo \"{updatedModel.getModelId()}\" actualizado!</div>")
            # return redirect(url_for("adminModels"))
            return "0"
    else:
        return redirect(url_for("adminModels"))

# Se usa el método HTTP DELETE para acceder a esta dirección, se maneja mediante ajax en JavaScript (src/templates/auth/adminModels.html)
# Se borra el recurso de modelo desde la base de datos
@app.route("/deleteModel", methods=["DELETE", "GET"])
def deleteModel():
    if request.method == "DELETE":
        modelId = json.loads(request.get_data())

        if model3DDAO.deleteModel3D(db, modelId) == 1:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema inesperado... </div>")
            return "1"

        else:
            flash(f"<div class=\"alert alert-success\" role=\"alert\"> Modelo \"{modelId}\" eliminado!</div>")
            return "0"
    else:
        return redirect(url_for("adminModels"))
# Fin de Ejemplo de Arquitectura REST
# -------------------------------------------------------------------------------

# Materiales
@app.route("/addMaterial", methods=["GET", "POST"])
def addMaterial():
    if request.method == "POST":
        newId = request.form['newMaterialId']
        newName = request.form['newMaterialName']
        newPriceModifier = request.form['newMaterialPriceModifier']
        newMaterial = material(newId, newName, newPriceModifier)
        regresar = 0

        if len(newMaterial.getMaterialId()) == 0:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El id no puede estar vacío </div>")
            regresar = 1
        if len(newMaterial.getMaterialName()) == 0:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El nombre no puede estar vacío </div>")
            regresar = 1
        try:
            if float(newMaterial.getMaterialPriceModifier()) <= 0:
                flash("<div class=\"alert alert-danger\" role=\"alert\"> El modificador de precio no puede ser 0 o menor </div>")
                regresar = 1
        except Exception as ex:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El modificador de precio debe ser un número valido  </div>")
            regresar = 1

        if regresar != 0:
            return redirect(url_for("adminMaterials"))
        if materialDAO.insertMaterial(db, newMaterial) == 1:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El id del nuevo material ya existe </div>")
        else:
            flash("<div class=\"alert alert-success\" role=\"alert\"> Material agregado! </div>")

        return redirect(url_for("adminMaterials"))
    else:
        return redirect(url_for("adminMaterials"))
    
@app.route("/updateMaterial", methods=["GET", "POST"])
def updateMaterial():
    if request.method == "POST":
        currentId = request.form['materialId']
        newName = request.form['newMaterialName']
        newPriceMod = request.form['newMaterialPriceModifier']

        updatedMaterial = material(currentId, newName, float(newPriceMod))

        if len(updatedMaterial.getMaterialName()) == 0 or updatedMaterial.getMaterialPriceModifier() <= 0 or materialDAO.updateMaterial(db, updatedMaterial) == 1:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema al actualizar... </div>")
        else:
            flash("<div class=\"alert alert-success\" role=\"alert\"> Material actualizado! </div>")

        return redirect(url_for("adminMaterials"))
    else:
        return redirect(url_for("adminMaterials"))

@app.route("/deleteMaterial", methods=["GET", "POST"])
def deleteMaterial():
    if request.method == "POST":
        materialId = request.form['materialId']

        newMaterial = material(materialId, "", "")
        try:
            if materialDAO.deleteMaterial(db, newMaterial.getMaterialId()) == 1:
                flash("<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema al eliminar... </div>")
            else:
                flash("<div class=\"alert alert-success\" role=\"alert\"> Material eliminado! </div>")
        except Exception as ex:
            flash( "<div class=\"alert alert-success\" role=\"alert\">" + str(Exception(ex)) + "</div>")
        return redirect(url_for("adminMaterials"))
    else:
        return redirect(url_for("adminMaterials"))

# Materiales Validos
@app.route("/addValidMaterial", methods=["GET", "POST"])
def addValidMaterials():
    if request.method == "POST":
        newModelKey = request.form['inputValidModel']
        newMaterialKey = request.form['inputValidMaterial']
        vinculo = validMaterial(newModelKey, newMaterialKey)
        if newModelKey == "nada" or newMaterialKey == "nada":
            flash("<div class=\"alert alert-danger\" role=\"alert\"> No hay registros para relacionar </div>")
            return redirect(url_for("adminValidMaterials"))
        if validMaterialDAO.insertValidMaterial(db, vinculo) == 1:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> La relación ya existe </div>")
        else:
            flash("<div class=\"alert alert-success\" role=\"alert\"> Relación agregada! </div>")
        return redirect(url_for("adminValidMaterials"))
    else:
        return redirect(url_for("adminValidMaterials"))

@app.route("/deleteValidMaterial", methods=["GET", "POST"])
def deleteValidMaterial():
    if request.method == "POST":
        modelKey = request.form['modelKey']
        materialKey = request.form['materialKey']
        eliminado = validMaterial(modelKey, materialKey)
        try:
            if validMaterialDAO.deleteValidMaterial(db,eliminado) == 1:
                flash("<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema al eliminar... </div>")
            else:
                flash("<div class=\"alert alert-success\" role=\"alert\"> Relación eliminada! </div>")
        except Exception as ex:
            flash("<div class=\"alert alert-danger\" role=\"alert\">" + str(Exception(ex)) + "</div>")
        return redirect(url_for("adminValidMaterials"))
    else:
        return redirect(url_for("adminValidMaterials"))
    
# Usuarios
@app.route("/addUser", methods=["GET", "POST"])
def addUser():
    if request.method == "POST":
        newUsername = request.form['inputNewUserName']
        newUsertype = int(request.form['inputNewUserType'])
        newPassword = request.form['inputNewUserPassword']
        newUser = user(newUsername, newUsertype, newPassword)
        regresar = 0
        try:
            if len(newUser.getUserName()) == 0 or len(newUser.getUserName()) > 100:
                flash("<div class=\"alert alert-danger\" role=\"alert\"> El nombre debe ser tener entre 1 y 100 caracteres </div>")
                regresar = 1
            if len(newUser.getUserPassword()) == 0:
                flash("<div class=\"alert alert-danger\" role=\"alert\"> La contraseña no puede estar vacía </div>")
                regresar = 1
            if regresar != 0:
                return redirect(url_for("adminUsers"))
            if UserDAO.addUser(newUser) == 1:
                flash("<div class=\"alert alert-danger\" role=\"alert\"> El usuario ya existe </div>")
            else:
                flash("<div class=\"alert alert-success\" role=\"alert\"> Usuario agregado! </div>")
            
        except Exception as ex:
            flash("<div class=\"alert alert-danger\" role=\"alert\">" + str(Exception(ex)) + "</div>")
        
        return redirect(url_for("adminUsers"))
    else:
        return redirect(url_for("adminUsers"))

@app.route("/updateUser", methods=["GET", "POST"])
def updateUser():
    if request.method == "POST":
        currentUsername = request.form['currentUserName']
        newUsername = request.form['newUsername']
        newUserType = int(request.form['newUserType'])

        try:
            if len(newUsername) == 0:
                flash("<div class=\"alert alert-danger\" role=\"alert\"> El nombre no puede estar vacío </div>")
            
            if current_user.getUserName() == currentUsername:
                flash("<div class=\"alert alert-danger\" role=\"alert\">" + "No puedes modificar al usuario activo" + "</div>")
                return redirect(url_for("adminUsers"))
            resultado = UserDAO.updateUser(db, currentUsername, newUsername, newUserType)

            if resultado == 1:
                flash("<div class=\"alert alert-danger\" role=\"alert\">" + "El usuario no existe" + "</div>")
            if resultado == 2:
                flash("<div class=\"alert alert-danger\" role=\"alert\">" + "El nuevo nombre de usuario ya existe" + "</div>")
            if resultado == 0:
                flash("<div class=\"alert alert-success\" role=\"alert\">" + "Usuario modificado" + "</div>")
        except Exception as ex:
            flash("<div class=\"alert alert-danger\" role=\"alert\">" + str(Exception(ex)) + "</div>")
        return redirect(url_for("adminUsers"))
    else:
        return redirect(url_for("adminUsers"))
    
@app.route("/deleteUser", methods=["GET", "POST"])
def deleteUser():
    if request.method == "POST":
        deletedUsername = request.form['currentUserName']
        if current_user.getUserName() == deletedUsername:
            flash("<div class=\"alert alert-danger\" role=\"alert\">" + "No puedes eliminar al usuario activo" + "</div>")
            return redirect(url_for("adminUsers"))
        
        try:
            if UserDAO.deleteUser(deletedUsername) == 1:
                flash("<div class=\"alert alert-danger\" role=\"alert\">" + "El usuario no existe" + "</div>")
            else:
                flash("<div class=\"alert alert-success\" role=\"alert\">" + "Usuario eliminado" + "</div>")
        except Exception as ex:
            flash("<div class=\"alert alert-danger\" role=\"alert\">" + str(Exception(ex)) + "</div>")
        return redirect(url_for("adminUsers"))
    else:
        return redirect(url_for("adminUsers"))
    
# AGREGAR ELEMENTO DEL CATALOGO
@app.route("/addOrderModel", methods=["GET", "POST"])
def addOrderModel():
    if request.method == "POST":
        # Separar el carrito sin cuenta del anónimo
        username = ""
        if current_user.is_authenticated:
            username = current_user.getUserName()
        if f'carrito{username}' not in session:
            session[f'carrito{username}'] = []
        # Obtener el carrito para el usuario
        carrito = session[f'carrito{username}']
        
        isCustom = False
        modelQty = request.form['modelQty']
        try:
            # Asegurar que la cantidad no este vacía
            modelQty = int(request.form['modelQty'])
            if modelQty < 1:
                raise Exception(ex)
        except Exception as ex:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema al agregar... </div>")
            return redirect(url_for("catalogo"))

        modelID = request.form['modelId']
        modelo = model3DDAO.getModelData(db, modelID)
        materialId = request.form['modelMaterialId']
        material = materialDAO.getMaterialData(db, materialId)

        newOrderModel = orderModel(isCustom, modelo.getModelId(), modelo.getModelName(), modelo.getModelFile(), modelo.getModelBasePrice(), modelQty, material.getMaterialId(), material.getMaterialName(), material.getMaterialPriceModifier())

        for model in carrito:
            if model['modelKey'] == newOrderModel.getModelKey() and model['materialKey'] == newOrderModel.getMaterialKey():
                model['modelQty'] = int(model['modelQty']) + int(newOrderModel.getModelQty())
                break
        else:
            carrito.append(newOrderModel.toDict())
            
        session[f'carrito{username}'] = carrito

        return redirect(url_for("catalogo"))
    else:
        return redirect(url_for("catalogo"))
    
@app.route("/addCustomModel", methods=["GET", "POST"])
def addCustomModel():
    if request.method == "POST":
        # Separar el carrito sin cuenta del anónimo
        username = ""
        if current_user.is_authenticated:
            username = current_user.getUserName()
        if f'carrito{username}' not in session:
            session[f'carrito{username}'] = []
        # Obtener el carrito para el usuario
        carrito = session[f'carrito{username}']

        modelId = request.form['modelId']
        modelName = request.form['modelName']
        modelFile = request.form['modelFile']
        modelQty = request.form['modelQty']
        modelMaterialId = request.form['modelMaterialId']
        modelPrice = round(random.uniform(3,15), 2)
        isCustom = True
        regresar = 0
        
        # VALIDACIONES DE CAMPOS
        if len(modelId) == 0:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El identificador no puede estar vacío... </div>", "warning")
            regresar = 1
        if len(modelId) > 15:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El identificador no puede ser mayor a 15 caracteres... </div>", "warning")
            regresar = 1
        if len(modelName) == 0:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El nombre no puede estar vacío... </div>", "warning")
            regresar = 1
        if len(modelName) > 255:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El nombre no puede ser mayor a 255 caracteres... </div>", "warning")
            regresar = 1
        if len(modelFile) == 0:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El archivo no puede estar vacío... </div>", "warning")
            regresar = 1
        if len(modelFile) > 255:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El archivo no puede ser mayor a 255 caracteres... </div>", "warning")
            regresar = 1
        if modelMaterialId == "nada":
            flash("<div class=\"alert alert-danger\" role=\"alert\"> No hay materiales para asignar... </div>", "warning")
            regresar = 1
        if model3DDAO.getModelData(db, modelId) != 1:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El identificador ya esta ocupado... </div>", "warning")
            regresar = 1

        try:
            if int(request.form['modelQty']) < 1:
                raise Exception(ex)
        except Exception as ex:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> Se debe agregar una cantidad valida... </div>", "warning")
            return redirect(url_for('pedidosPersonalizados'))
        if regresar != 0:
            return redirect(url_for('pedidosPersonalizados'))
        else:
            # AGREGAR AL CARRITO
            material = materialDAO.getMaterialData(db, modelMaterialId)
            newOrderModel = orderModel(isCustom, modelId, modelName, modelFile, modelPrice, modelQty, modelMaterialId, material.getMaterialName(), material.getMaterialPriceModifier())

            for model in carrito:
                if model['modelKey'] == newOrderModel.getModelKey() and model['materialKey'] == newOrderModel.getMaterialKey():
                    model['modelQty'] = int(model['modelQty']) + int(newOrderModel.getModelQty())
                    flash("<div class=\"alert alert-success\" role=\"alert\"> Como el modelo ya estaba en carrito, se ha sumado su cantidad... </div>", "warning")
                    break
            else:
                carrito.append(newOrderModel.toDict())
            flash("<div class=\"alert alert-success\" role=\"alert\"> Modelo agregado al carrito! </div>", "warning")
            session[f'carrito{username}'] = carrito
            return redirect(url_for('pedidosPersonalizados'))
    else:
        return redirect(url_for('pedidosPersonalizados'))
    
@app.route("/clearSession", methods=["GET", "POST"])
def clearSession():
    username = ""
    if current_user.is_authenticated:
        username = current_user.getUserName()
        session[f'carrito{username}'] = []
    else:
        session.clear()
    return redirect(url_for('pedidosPersonalizados'))

@app.route("/deleteFromOrder", methods=["GET", "POST"])
def deleteFromOrder():
    if request.method == "POST":
        username = ""
        if current_user.is_authenticated:
            username = current_user.getUserName()
        if f'carrito{username}' not in session:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> El carrito esta vacío  </div>", "warning")
            redirect(url_for('pedidosPersonalizados'))

        # Obtener el carrito para el usuario
        carrito = session[f'carrito{username}']
        modelKey = request.form['modelKey']
        materialKey = request.form['materialKey']

        for index, elemento in enumerate(carrito):
            if elemento['modelKey'] == modelKey and elemento['materialKey'] == materialKey:
                carrito.pop(index)
                break
        session[f'carrito{username}'] = carrito
        flash("<div class=\"alert alert-success\" role=\"alert\"> Se ha eliminado del carrito  </div>", "warning")
        return redirect(url_for('pedidosPersonalizados'))
    else:
        return redirect(url_for('pedidosPersonalizados'))

@app.route("/confirmOrder", methods=["GET", "POST"])
def confirmOrder():
    if request.method == "POST":
        username = ""
        if current_user.is_authenticated:
            username = current_user.getUserName()
        if f'carrito{username}' not in session:
            flash('<p class="alert alert-danger"> El carrito no puede estar vacío </p>', "warning")
            redirect(url_for('pedidosPersonalizados'))
        carrito = session[f'carrito{username}']

        # SI NO HAY CARRITO, NO HACER NADA
        if len(carrito) == 0:
            flash('<p class="alert alert-danger"> El carrito no puede estar vacío </p>', "warning")
            return redirect(url_for('pedidosPersonalizados'))

        if username == "":
            username = None

        if len(request.form['orderAddress']) != 0:
            orderId = orderModelDAO.confirmOrder(db, carrito, username, request.form['orderAddress'])
            flash(f'<p class="alert alert-success"> Pedido confirmado!<br>Tu ID de pedido es: {orderId}<br>Si no posee una cuenta es importante que guarde este Id para consultar su pedido</p>', "warning")
            if username == None:
                username = ""
            session[f'carrito{username}'] = []
        else:
            flash('<p class="alert alert-danger"> Favor de ingresar dirección de entrega </p>', "warning")
        return redirect(url_for('pedidosPersonalizados'))
    else:
        return redirect(url_for('pedidosPersonalizados'))
    
@app.route("/searchOrder", methods=["GET", "POST"])
def searchOrder():
    pedido = orderDAO.getOrderFromId(db, request.form['orderId'])
    if pedido == None:
        flash('<p class="alert alert-danger"> Pedido no válido </p>', "info")
        return redirect(url_for('pedidosPersonalizados'))
    
    orderListHTML = auxMethods.generateSearchCustomOrder(db, pedido)

    flash(orderListHTML, "info")
    return redirect(url_for('pedidosPersonalizados'))

# En caso de ingresar una ruta que no existe
@app.errorhandler(404)
def rutaInexistente(e):
    return redirect(url_for('iniciarSesion'))

# Web Service

@app.route('/soap/addUser', methods=['GET', 'POST'])
def soapAddUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        userType = int(request.form['usertype'])

        if len(username) < 1 or len(password) < 1:
            flash('Los datos deben estar completos')
            return redirect(url_for('soapAddUser'))
        
        # Llamar al servicio SOAP para agregar el usuario
        try:
            with app.app_context():
                client = Client('http://localhost:5001/soap?wsdl')
                resultado = client.service.addUser(username, password, userType)
            # Redirigir a alguna página de éxito o mostrar un mensaje de éxito
            if resultado == 0:
                flash(f'Código de salida: {resultado}\nUsuario Agregado')
            else:
                flash(f'Código de salida: {resultado}\nError en registro')
            return redirect(url_for('soapAddUser'))
        except Exception as ex:
            return str(ex)
    if request.method == 'GET':
        # Mostrar el formulario para agregar usuario
        try:
            with app.app_context():
                cliente = Client('http://localhost:5001/soap?wsdl')
                usersList = json.loads(cliente.service.showUsers())

                usersListHTML = auxMethods.generateSOAPUsersList(usersList)

            return render_template('auth/AddUserSOAP.html', usersListHTML=usersListHTML)
        except Exception as ex:
            return str(ex)
        
# Eliminar usuarios con SOAP
@app.route('/soap/deleteUser', methods=['GET', 'POST'])
def soapDeleteUser():
    if request.method == 'POST':
        resultado = 1
        print("Acceso a SOAP: soapDeleteUser()")
        try:
            with app.app_context():
                cliente = Client('http://localhost:5001/soap?wsdl')
                resultado = cliente.service.deleteUser(request.form['currentUser'])

                if (resultado == 1):
                    flash(f'Código de salida: {resultado}\nError en eliminación')
                else:
                    flash(f'Código de salida: {resultado}\nEliminación exitosa')
            return redirect(url_for('soapAddUser'))
        except Exception as ex:
            flash(f'Código de salida: {resultado}\nError en registro')
    else:
        return redirect(url_for('soapAddUser'))

@app.route('/soap/updateUser', methods=['GET', 'POST'])
def soapUpdateUser():
    if request.method == "POST":
        print("Acceso a SOAP: soapUpdateUser()")

        try:
            with app.app_context():
                cliente = Client('http://localhost:5001/soap?wsdl')
                resultado = cliente.service.updateUser(request.form['currentUser'], request.form['newUserName'], int(request.form['newUserType']))
                if (resultado == 1):
                    flash(f'Código de salida: {resultado}\nActualización fallida')
                else:
                    flash(f'Código de salida: {resultado}\nActualización exitosa')
            return redirect(url_for('soapAddUser'))
        except Exception as ex:
            return redirect(url_for('soapAddUser'))
    else:
        return redirect(url_for('soapAddUser'))

# Iniciar servidor SOAP
def initSOAP():
    from wsgiref.simple_server import make_server
    spyne_app = Application([UserService], 'soap.addUser', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
    spyne_wsgi_app = WsgiApplication(spyne_app)

    spyne_server = make_server('localhost', 5001, spyne_wsgi_app)
    print('Servidor SOAP iniciado: http://localhost:5001/soap')
    spyne_server.serve_forever()

# Iniciar servidor Flask
def initFlask():
    try:
        print('Servidor Flask iniciado: http://localhost:5000')
        app.config.from_object(config['development'])
        app.run(debug=True)
    except Exception as ex:
        print(f'Error al iniciar servidor: {ex}')


# Al ejecutar app.py -> inicia el servidor
if __name__ == "__main__":
    soap_thread = threading.Thread(target=initSOAP)

    soap_thread.start()
    initFlask()