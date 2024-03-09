from .user import user

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

