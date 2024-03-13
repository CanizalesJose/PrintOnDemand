from .user import user
from .userType import userType

class UserDAO():

    @classmethod
    def login(self, db, usuario):
        try:
            cursor = db.connection.cursor()
            cursor.execute("call iniciarSesion(%s, %s)", (usuario.getUserName(), usuario.getUserPassword()))
            row = cursor.fetchone()
            if row[0] != None:
                usuario = user(row[0], row[1], row[2])
                return usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def get_by_name(self, db, userName):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select userName, userType, userPassword from users where userName = %s", (userName,))
            row = cursor.fetchone()
            if row[0] != None:
                usuario = user(row[0], row[1], row[2])
                return usuario
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def getFullUserData(self, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select userName, usertype, userpassword, typeId, userTypeName from users inner join usertypes on users.usertype = usertypes.typeid")
            resultados = cursor.fetchall()
            fullUserList = []
            for registro in resultados:
                fullUserList.append({
                    'usuario' : user(registro[0], registro[1], 'oculta'),
                    'usertype' : userType(registro[3], registro[4])
                    })

            return fullUserList
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()