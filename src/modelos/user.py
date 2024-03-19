from flask_login import UserMixin
class user(UserMixin):

    def __init__(self, userName: str, userType: int, userPassword: str):
        self._userName = userName
        self._userType = userType
        self._userPassword = userPassword

# Comienzan los getters y setters

    def get_id(self):
        # Devuelve el identificador único del usuario como una cadena
        return str(self._userName)
    
    def getUserName(self) -> str:
        return self._userName
    def setUserName(self, newUserName) -> None:
        self._userName = newUserName

    def getUserType(self) -> int:
        return self._userType
    def setUserType(self, newUserType) -> None:
        self._userType = newUserType

    def getUserPassword(self) -> str:
        return self._userPassword
    def setUserPassword(self, newUserPassword) -> None:
        self._userPassword = newUserPassword