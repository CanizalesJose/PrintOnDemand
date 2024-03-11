from .model3D import Model3D

class model3DDAO():

    @classmethod
    def getValidModel(self, db, inputModelId):
        try:
            cursor = db.connection.cursor()
            cursor.execute("call showCatalogData(%s)", (inputModelId,))

            resultado = cursor.fetchone()
            return resultado
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()
    
    @classmethod
    def showAllModelId(self, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("call showAllModelId()")
            resultados = cursor.fetchall()
            modelsIds = []
            for linea in resultados:
                linea = linea[0]
                modelsIds.append(linea)
            return modelsIds
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def getMaterialsFromModel(self,db, inputModelId):
        try:
            cursor = db.connection.cursor()
            cursor.execute("call getMaterialsFromModel(%s)", (inputModelId,))
            resultados = cursor.fetchall()
            materials = []
            for linea in resultados:
                registro = {
                    "materialId" : linea[0],
                    "materialName" : linea[1],
                    "materialPriceModifier" : linea[2]
                }
                materials.append(registro)

            print(resultados)
            return materials
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()