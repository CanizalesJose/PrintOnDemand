from spyne import rpc, ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from modelos.UserDAO import UserDAO
from modelos.user import user

class UserService(ServiceBase):
    @rpc(str, str, int, _returns=int)
    def addUser(ctx, username, password, userType):
        newUser = user(username, userType, password)
        resultado = UserDAO.addUser(newUser)
        return resultado