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
    
    @rpc(_returns=str)
    def deleteUser(ctx, username):
        try:
            db = Conexion.generarConexion()
        except Exception as ex:
            raise Exception(ex)
