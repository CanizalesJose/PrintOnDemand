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
            return materials
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def getAllModels(self, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("call getAllModels()")
            resultados = cursor.fetchall()
            modelsList = []
            for registro in resultados:
                modelo = Model3D(registro[0], registro[1], registro[2], registro[3], registro[4])
                modelsList.append(modelo)
            return modelsList
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def insertModel3D(self, db, modelo):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select modelId from models3d where modelId=%s", (modelo.getModelId(),))
            consulta = cursor.fetchone()
            if consulta != None:
                return 1
            cursor.execute("insert into models3d (modelId, modelName, modelImage, modelFile, modelBasePrice) values (%s, %s, %s, %s, %s)", (modelo.getModelId(), modelo.getModelName(), modelo.getModelImage(), modelo.getModelFile(), float(modelo.getModelBasePrice())))
            db.connection.commit()
            return 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()
    
    @classmethod
    def updateModel3D(self, db, modelo):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select modelId from models3D where modelId = %s", (modelo.getModelId(),))
            consulta = cursor.fetchone()
            if consulta == None:
                return 1
            else:
                cursor.execute("update models3D set modelName = %s, modelImage = %s, modelFile = %s, modelBasePrice = %s where modelId = %s", (modelo.getModelName(), modelo.getModelImage(), modelo.getModelFile(), float(modelo.getModelBasePrice()), modelo.getModelId()))
                db.connection.commit()
                return 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()
    
    @classmethod
    def deleteModel3D(self, db, modelId):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select modelId from models3D where modelId = %s", (modelId, ))
            consulta = cursor.fetchone()
            if consulta == None:
                return 1
            else:
                cursor.execute("call deleteModel3D(%s)", (modelId, ))
                db.connection.commit()
                return 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()