from spyne import rpc, ServiceBase
from modelos.UserDAO import UserDAO
from modelos.user import user
from config.Conexion import Conexion
from modelos.deliveryMicroservice import deliveryMicroservice
import json

class UserService(ServiceBase):
    @rpc(str, str, int, _returns=int)
    def addUser(ctx, username, password, userType):
        newUser = user(username, userType, password)
        resultado = UserDAO.addUser(newUser)
        return resultado
    
    @rpc(_returns=str)
    def showUsers(ctx):
        usersList = UserDAO.getFullUserData()
        lista = []
        for user in usersList:
            nuevo = {'user' : {'username' : user['usuario'].getUserName(), 'usertype' : user['usuario'].getUserType()}, 'usertype' : {'usertypeid' : user['usertype'].getUserTypeId(), 'usertypename' : user['usertype'].getUserTypeName()}}
            lista.append(nuevo)
        return json.dumps(lista)
    
    @rpc(str, _returns=int)
    def deleteUser(ctx, username):
        try:
            db = Conexion.generarConexion()
            cursor = db.cursor()
            cursor.execute("call deleteUser(%s)", (username, ))
            db.commit()
            cursor.close()
            return 0
        except Exception as ex:
            return 1

    @rpc(str, str, int, _returns=int)
    def updateUser(ctx, currentUser, newUser, usertype):
        try:
            db = Conexion.generarConexion()
            cursor = db.cursor()
            cursor.execute("call updateUser(%s, %s, %s)", (currentUser, newUser, usertype))
            db.commit()
            cursor.close()
            return 0
        except Exception as ex:
            return 1
    
    @rpc(str, _returns=str)
    def searchDelivery(ctx, username):
        try:
            resultado = deliveryMicroservice.showUserDelivery(username)
            return resultado
        except Exception as ex:
            return ""