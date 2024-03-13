from .userType import userType

class userTypeDAO():
    @classmethod
    def getUserTypes(self, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select typeId, userTypeName from userTypes")
            resultados = cursor.fetchall()
            userTypesList = []
            for registro in resultados:
                userTypesList.append(userType(registro[0], registro[1]))

            return userTypesList
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()