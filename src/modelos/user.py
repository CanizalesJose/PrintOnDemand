from flask_login import UserMixin
class user(UserMixin):

    def __init__(self, userName, userType, userPassword) -> None:
        self._userName = userName
        self._userType = userType
        self._userPassword = userPassword

# Comienzan los getters y setters

    def get_id(self):
        # Devuelve el identificador único del usuario como una cadena
        return str(self._userName)

    def getUserName(self):
        return self._userName

    def setUserName(self, newUserName):
        self._userName = newUserName

    def getUserType(self):
        return self._userType

    def setUserType(self, newUserType):
        self._userType = newUserType

    def getUserPassword(self):
        return self._userPassword
    
    def setUserPassword(self, newUserPassword):
        self._userPassword = newUserPassword