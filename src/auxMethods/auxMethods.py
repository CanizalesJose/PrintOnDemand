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
import json
from modelos.deliveryMicroservice import deliveryMicroservice

class auxMethods():

    @classmethod
    def generateCatalog(self, db):
        # Recorre cada modelo
        catalogo = ""
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
        return catalogo

    @classmethod
    def generateModelList(self, db):
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
                        <form id="updateForm{modelo.getModelId()}">
                            <input type="hidden" name="modelId" value="{modelo.getModelId()}">
                            <div class="form-floating mb-1">
                                <input type="text" class="form-control" id="updatedModelName{modelo.getModelId()}" name="updatedModelName" value="{modelo.getModelName()}">
                                <label>Nuevo nombre</label>
                            </div>

                            <div class="form-floating mb-1">
                                <input type="text" class="form-control" id="updatedModelImage{modelo.getModelId()}" name="updatedModelImage" value="{modelo.getModelImage()}">
                                <label>Nueva Imagen</label>
                            </div>

                            <div class="form-floating mb-1">
                                <input type="text" class="form-control" id="updatedModelFile{modelo.getModelId()}" name="updatedModelFile" value="{modelo.getModelFile()}">
                                <label>Nuevo archivo</label>
                            </div>

                            <div class="form-floating mb-1">
                                <input type="number" step="0.01" class="form-control" id="updatedModelBasePrice{modelo.getModelId()}" name="updatedModelBasePrice" value="{modelo.getModelBasePrice()}">
                                <label>Nuevo precio base</label>
                            </div>

                            <button type="button" class="btn btn-primary bg-gradient mt-3" onclick='updateModel("{modelo.getModelId()}")'>Modificar</button>
                        </form>

                        <form id="deleteForm{modelo.getModelId()}">
                            <input type="hidden" name="modelId" value="{modelo.getModelId()}">
                            <button type="button" class="btn btn-danger bg-gradient mt-3" onclick='deleteModel("{modelo.getModelId()}")'>Eliminar</button>
                        </form>
                    </td>
                </tr>
                """
        return listaModelosHTML

    @classmethod
    def generateUserLists(self, db):
        userTypesListHTML = ""
        userTypesList = userTypeDAO.getUserTypes(db)
        for registro in userTypesList:
            userTypesListHTML += f"""
                <option value="{registro.getUserTypeId()}">{registro.getUserTypeName()}</option>
            """
        # Generar la lista de usuarios registrados
        usersList = UserDAO.getFullUserData()
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
        return [userTypesListHTML, userListHTML]
    
    @classmethod
    def generateMaterialsList(self, db):
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
        return materialsListHTML
    
    @classmethod
    def generateValidMaterialsLists(self, db):
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
        return [validModelsOptionsHTML, materialsListHTML, validListHTML]
    
    @classmethod
    def generateCustomOrders(self, db, carrito, current_user):
        materialsListHTML = ""
        listaResumenHTML = ""
        totalResumen = 0
        orderListHTML= ""

        # Generar lista de materiales
        materialsList = materialDAO.getAllMaterials(db)
        if materialsList != None:
            for material in materialsList:
                materialsListHTML += f"""
                    <option value="{material.getMaterialId()}">{material.getMaterialName()} ($ x {material.getMaterialPriceModifier()})</option>
                """
        else:
            materialsListHTML = "<option value=\"nada\">No hay registros</option>"
        
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
                                        <th scope="col">Nombre del modelo</th>
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
                try:
                    orderListHTML+= deliveryMicroservice.showDeliveryStatus(pedido.getOrderId())
                except Exception as ex:
                    print("No se ha encontrado pedido")
        else:
            orderListHTML = ""

        return[materialsListHTML, listaResumenHTML, totalResumen, orderListHTML]
    
    @classmethod
    def generateSearchCustomOrder(self, db, pedido):
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
        return orderListHTML
    
    @classmethod
    def generateSOAPUsersList(self, usersList):
        userListHTML = ''
        auxUsers = ''
        usersListHTML = ''

        for user in usersList:
            auxUsers += f"""
                <tr>
                    <td>{user['user']['username']}</td>
                    <td>{user['usertype']["usertypename"]}</td>
                </tr>
            """
            # Fin de For
        userListHTML += f"""
        <table class="table table-hover text-center">
            <thead>
                <tr>
                    <th>UserName</th>
                    <th>UserType</th>
                </tr>
            </thead>
            <tbody>
                {auxUsers}
            </tbody>
        </table>
        """
        return userListHTML
        try:
            orderListHTML += deliveryMicroservice.showDeliveryStatus(pedido.getOrderId())
        except Exception as ex:
            print("No se pudo conectar al microservicio de entregas...")
        return orderListHTML
