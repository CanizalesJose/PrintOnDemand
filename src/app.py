# Importar librerias
from flask import Flask, render_template, redirect, request, url_for, flash, get_flashed_messages, abort, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from config.config import config
import random
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
from modelos.order import order
from modelos.orderDAO import orderDAO


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
            flash("""
            <div class="alert alert-danger" role="alert">
                Usuario o contraseña incorrectos...
            </div>
            """)
            return render_template('auth/InicioSesion.html')
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
                <option value="{material["materialId"]}">{material["materialName"]} ($ x {material["materialPriceModifier"]})</option>
                """

            catalogo = catalogo + f"""
             <div class="col-lg-3 my-4">
                    <div class="card text-dark rounded">
                        <img src="{validModel[2]}" class="card-img-top imgArticulo" alt="Producto {validModel[0]}">
                        <div class="card-body">
                            <h5 class="card-title">{validModel[1]}</h5>
                            <p class="card-text">$ {validModel[4]}</p>

                            <form action="/addOrderModel" method="POST">
                                <input type="text" class="form-control" name="modelId" value="{validModel[0]}" hidden>

                                <div class="form-floating mb-3 mx-5">
                                    <input type="number" class="form-control" name="modelQty" placeholder="Cantidad" value="1">
                                    <label>Cantidad:</label>
                                </div>

                                <div class="form-floating mb-3 mx-5">
                                    <select class="form-select" name="modelMaterialId">
                                        {materialsList}
                                    </select>
                                    <label>Seleccionar material: </label>
                                </div>

                                <div class="text-center">
                                    <button type="submit" class="btn btn-primary agregar">Agregar al carrito</button>
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
        listaModelosHTML = ""
        listaModelos = model3DDAO.getAllModels(db)
        if listaModelos != None:
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
                                <label>Nuevo nombre</label>
                            </div>

                            <div class="form-floating mb-1">
                                <input type="text" class="form-control" name="updatedModelImage" value="{modelo.getModelImage()}">
                                <label>Nueva Imagen</label>
                            </div>

                            <div class="form-floating mb-1">
                                <input type="text" class="form-control" name="updatedModelFile" value="{modelo.getModelFile()}">
                                <label>Nuevo archivo</label>
                            </div>

                            <div class="form-floating mb-1">
                                <input type="number" step="0.01" class="form-control" name="updatedModelBasePrice" value="{modelo.getModelBasePrice()}">
                                <label>Nuevo precio base</label>
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
        return render_template("auth/adminModels.html", listaModelosHTML=listaModelosHTML)
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
                    <form action="/updateUser" method="POST">
                        <input type="hidden" name="currentUserName" value="{registro['usuario'].getUserName()}">

                        <div class="form-floating mb-1">
                            <input type="text" class="form-control" name="newUsername" value="{registro['usuario'].getUserName()}">
                            <label>Nuevo nombre</label>
                        </div>
                        
                        <div class="form-floating mb-1">
                            <select class="form-select" aria-label="Seleccion de tipo" name="newUserType" placeholder="newUserType">
                                {userTypesListHTML}
                            </select>
                            <label>Tipo de usuario</label>
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
        
        return render_template("auth/adminUsers.html", userTypesListHTML=userTypesListHTML, userListHTML=userListHTML)
    else:
        return redirect('catalogo')

@app.route("/adminMaterials")
def adminMaterials():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        materialsList = materialDAO.getAllMaterials(db)
        materialsListHTML = ""
        if materialsList != None:
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
                                <label>Nuevo Nombre</label>
                            </div>

                            <div class="form-floating mb-1">
                                <input type="number" step="0.01" class="form-control" name="newMaterialPriceModifier" placeholder="price" value="{material.getMaterialPriceModifier()}">
                                <label>Multiplicador de precio</label>
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
        return render_template("auth/adminMaterials.html", materialsListHTML=materialsListHTML)
    else:
        return redirect('catalogo')

@app.route("/adminValidMaterials")
def adminValidMaterials():
    if current_user.is_authenticated and current_user.getUserType() == 1:
        # Generar lista de modelos validos
        validModels = model3DDAO.getAllModels(db)
        validModelsOptionsHTML = ""
        if validModels != None:
            for modelo in validModels:
                validModelsOptionsHTML += f"""
                    <option value="{modelo.getModelId()}">{modelo.getModelName()}</option>
                """
        else:
            validModelsOptionsHTML = "<option value=\"nada\">No hay registros</option>"
        # Generar la lista de materiales
        materialsList = materialDAO.getAllMaterials(db)
        materialsListHTML = ""
        if materialsList != None:
            for material in materialsList:
                materialsListHTML += f"""
                    <option value="{material.getMaterialId()}">{material.getMaterialName()}</option>
                """
        else:
            materialsListHTML = "<option value=\"nada\">No hay registros</option>"
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

        return render_template("auth/adminValidMaterials.html", validModelsOptionsHTML=validModelsOptionsHTML, materialsListHTML=materialsListHTML, validListHTML=validListHTML)
    else:
        return redirect('catalogo')

@app.route("/pedidosPersonalizados")
def pedidosPersonalizados():
    materialsListHTML =""
    listaResumenHTML = ""
    totalResumen = 0
    # Generar lista de materiales
    materialsList = materialDAO.getAllMaterials(db)
    if materialsList != None:
        for material in materialsList:
            materialsListHTML += f"""
                <option value="{material.getMaterialId()}">{material.getMaterialName()} ($ x {material.getMaterialPriceModifier()})</option>
            """
    else:
        materialsListHTML = "<option value=\"nada\">No hay registros</option>"
    
    # Recuperar el carrito o crearlo
    username = ""
    if current_user.is_authenticated:
        username = current_user.getUserName()
    if f'carrito{username}' not in session:
        session[f'carrito{username}'] = []
    carrito = session[f'carrito{username}']

    # CONSTRUIR LA TABLA PARA DETALLES DE LA COMPRA
    for registro in carrito:
        totalResumen += int(registro['modelQty'])*float(registro['modelPrice'])*float(registro['materialPriceModifier'])
        listaResumenHTML += f"""
            <tr>
                <td>{registro['isCustom']}</td>
                <td>{registro['modelName']}</td>
                <td>{registro['materialName']} ($ x {registro['materialPriceModifier']})</td>
                <td>{registro['modelQty']}</td>
                <td>{registro['modelPrice']}</td>
                <td>{round(int(registro['modelQty'])*float(registro['modelPrice'])*float(registro['materialPriceModifier']), 2)}</td>
                <td>
                    <form action="/deleteFromOrder" method="POST">
                        <input name="modelKey" value="{registro['modelKey']}" hidden>
                        <input name="materialKey" value="{registro['materialKey']}" hidden>
                        <button type="submit" class="btn btn-danger bg-gradient my-3" onclick="return confirm('¿Estas seguro de eliminar modelo del carrito?')">Eliminar</button>
                    </form>
                </td>
            <tr>
        """
    totalResumen = round(totalResumen, 2)

    # CONSTRUIR LISTA DE PEDIDOS REALIZADOS SI ESTA REGISTRADO
    if current_user.is_authenticated:
        orderList = orderDAO.getOrderWithUser(db,current_user.getUserName())
        orderListHTML = ""
        for pedido in orderList:
            orderListHTML += f"""
                <h3 class="text-start">Id del pedido: {pedido.getOrderId()}</h3>
                <h6 class="text-start">Fecha del pedido: {pedido.getOrderDate()}</h6>
                <h5 class="text-start">Modelos del catalogo:</h5>
                <div class="overflow-scroll">
                        <table class="table table-hover text-center">
                            <thead>
                                <tr>
                                    <th scope="col">Model Id</th>
                                    <th scope="col">Archivo</th>
                                    <th scope="col">Modelo</th>
                                    <th scope="col">Material</th>
                                    <th scope="col">Qty.</th>
                                    <th scope="col">Precio</th>
                                    <th scope="col">Subtotal</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            for modelo in orderDAO.getModelsWithUser(db, current_user.getUserName(), pedido.getOrderId()):
                orderListHTML += f"""
                    <tr>
                        <td>{modelo['modelKey']}</td>
                        <td>{modelo['modelFile']}</td>
                        <td>{modelo['modelName']}</td>
                        <td>{modelo['materialName']}</td>
                        <td>{modelo['modelQty']}</td>
                        <td>{modelo['modelPrice']}</td>
                        <td>{modelo['subtotal']}</td>
                    </tr>
                """
            
            orderListHTML += f"""
                </tbody>
                    </table>
                </div>
                <br>
                <h5 class="text-start">Modelos Personalizados:</h5>
                    <div class="overflow-scroll">
                        <table class="table table-hover text-center">
                            <thead>
                                <tr>
                                    <th scope="col">Modelo</th>
                                    <th scope="col">Archivo</th>
                                    <th scope="col">Material</th>
                                    <th scope="col">Qty.</th>
                                    <th scope="col">Precio</th>
                                    <th scope="col">Subtotal</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            # Generar custom models table
            for modelo in orderDAO.getCustomModelsWithUser(db, current_user.getUserName(), pedido.getOrderId()):
                orderListHTML += f"""
                    <tr>
                        <td>{modelo['modelKey']}</td>
                        <td>{modelo['modelFile']}</td>
                        <td>{modelo['modelName']}</td>
                        <td>{modelo['materialName']}</td>
                        <td>{modelo['modelQty']}</td>
                        <td>{modelo['modelPrice']}</td>
                        <td>{modelo['subtotal']}</td>
                    </tr>
                """
            orderListHTML += f"""
                        </tbody>
                    </table>
                </div>
                <h6 class="text-end">Total: $ {pedido.getOrderTotalCost()}<h6>
                <h6 class="text-start">Dirección de entrega: {pedido.getOrderAddress()}</h6>
                <hr>
            """
    else:
        orderListHTML = ""
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

@app.route("/updateModel", methods=["POST", "GET"])
def updateModel():
    if request.method == "POST":
        modelId = request.form['modelId']
        modelName = request.form['updatedModelName']
        modelImage = request.form['updatedModelImage']
        modelFile = request.form['updatedModelFile']
        modelBasePrice = float(request.form['updatedModelBasePrice'])
        updatedModel = Model3D(modelId, modelName, modelImage, modelFile, modelBasePrice)

        if len(updatedModel.getModelId()) == 0 or len(updatedModel.getModelName()) == 0 or len(updatedModel.getModelImage()) == 0 or len(updatedModel.getModelFile()) == 0 or float(updatedModel.getModelBasePrice()) <= 0 or model3DDAO.updateModel3D(db, updatedModel) == 1:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema con los datos... </div>")
            return redirect(url_for("adminModels"))
        else:
            flash(f"<div class=\"alert alert-success\" role=\"alert\"> Modelo \"{updatedModel.getModelId()}\" actualizado!</div>")
            return redirect(url_for("adminModels"))
    else:
        return redirect(url_for("adminModels"))

@app.route("/deleteModel", methods=["POST", "GET"])
def deleteModel():
    if request.method == "POST":
        modelId = request.form['modelId']

        if model3DDAO.deleteModel3D(db, modelId) == 1:
            flash("<div class=\"alert alert-danger\" role=\"alert\"> Hubo un problema inesperado... </div>")
            return redirect(url_for("adminModels"))

        else:
            flash(f"<div class=\"alert alert-success\" role=\"alert\"> Modelo \"{modelId}\" eliminado!</div>")
            return redirect(url_for("adminModels"))
    else:
        return redirect(url_for("adminModels"))
    

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
            if UserDAO.addUser(db, newUser) == 1:
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
            if UserDAO.deleteUser(db, deletedUsername) == 1:
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
    orderListHTML = ""
    orderListHTML += f"""
        <h3 class="text-start">Id del pedido: {pedido.getOrderId()}</h3>
        <h6 class="text-start">Fecha del pedido: {pedido.getOrderDate()}</h6>
        <h5 class="text-start">Modelos del catalogo:</h5>
        <div class="overflow-scroll">
                <table class="table table-hover text-center">
                    <thead>
                        <tr>
                            <th scope="col">Model Id</th>
                            <th scope="col">Archivo</th>
                            <th scope="col">Modelo</th>
                            <th scope="col">Material</th>
                            <th scope="col">Qty.</th>
                            <th scope="col">Precio</th>
                            <th scope="col">Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    for modelo in orderDAO.getModelNoUser(db, pedido.getOrderId()):
        orderListHTML += f"""
            <tr>
                <td>{modelo['modelKey']}</td>
                <td>{modelo['modelFile']}</td>
                <td>{modelo['modelName']}</td>
                <td>{modelo['materialName']}</td>
                <td>{modelo['modelQty']}</td>
                <td>{modelo['modelPrice']}</td>
                <td>{modelo['subtotal']}</td>
            </tr>
        """
    
    orderListHTML += f"""
        </tbody>
            </table>
        </div>
        <h6 class="text-end">Total: $ {pedido.getOrderTotalCost()}<h6>
        <h6 class="text-start">Dirección de entrega: {pedido.getOrderAddress()}</h6>
        <hr>
    """
    flash(orderListHTML, "info")
    return redirect(url_for('pedidosPersonalizados'))

# En caso de ingresar una ruta que no existe
@app.errorhandler(404)
def rutaInexistente(e):
    return redirect(url_for('iniciarSesion'))


# Al ejecutar el archivo, inicia el servidor
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(use_reloader=True)