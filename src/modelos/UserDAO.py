from .user import user
from .userType import userType
from config.Conexion import Conexion

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
            if row != None:
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

    @classmethod
    def addUser(self, usuario):
        try:
            db = Conexion.generarConexion()
            cursor = db.cursor()
            cursor.execute("select * from users where username = %s", (usuario.getUserName(),))
            consulta = cursor.fetchone()
            if consulta != None:
                return 1
            else:
                cursor.execute("call registrarUser(%s, %s, %s)", (usuario.getUserName(), usuario.getUserPassword(), usuario.getUserType()))
                db.commit()
                return 0
        except Exception as ex:
            db.rollback()
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def updateUser(self, db, currentUsername, newUsername, newUserType):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select username from users where username = %s", (currentUsername, ))
            consulta = cursor.fetchone()
            if consulta == None:
                return 1
            if currentUsername != newUsername:
                cursor.execute("select username from users where username = %s", (newUsername, ))
                consulta = cursor.fetchone()
                if consulta != None:
                    return 2
            cursor.execute("call updateUser(%s, %s, %s)", (currentUsername, newUsername, newUserType))
            db.connection.commit()
            return 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def deleteUser(self, deletedUsername):
        try:
            db = Conexion.generarConexion()
            cursor = db.cursor()
            cursor.execute("select username from users where username = %s", (deletedUsername, ))
            consulta = cursor.fetchone()
            if consulta == None:
                return 1
            cursor.execute("call deleteUser(%s)", (deletedUsername, ))
            db.commit()
            return 0
        except Exception as ex:
            db.rollback()
            raise Exception(ex)
        finally:
            cursor.close()