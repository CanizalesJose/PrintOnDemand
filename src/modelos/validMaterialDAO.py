from .validMaterial import validMaterial
from .material import material
from .model3D import Model3D

class validMaterialDAO():
    @classmethod
    def getModelsIdWithMaterials(self, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select modelKey, modelName, modelImage from validMaterials inner join models3d on validMaterials.modelKey = models3d.modelId group by modelKey")
            resultado = cursor.fetchall()
            if resultado != None:
                modelsKeyList = []
                for registro in resultado:
                    nuevo = Model3D(registro[0], registro[1], registro[2], "", "")
                    modelsKeyList.append(nuevo)
                return modelsKeyList
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def getMaterialsFromModel(self, db, modelId):
        try:
            cursor = db.connection.cursor()
            # Buscar los materiales y su información en base al modelId
            cursor.execute("select materialKey, materialName, materialPriceModifier from validMaterials inner join materials on validMaterials.materialKey = materials.materialId where modelKey = %s", (modelId,))
            resultado = cursor.fetchall()
            if resultado != None:
                validMaterialsList = []
                for registro in resultado:
                    nuevo = material(registro[0], registro[1], registro[2])
                    validMaterialsList.append(nuevo)

                print(validMaterialsList)
                return validMaterialsList
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def getDataValidMaterials(self, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select modelKey, modelName, modelImage, materialKey, materialName from validMaterials inner join materials on validmaterials.materialKey = materials.materialId inner join models3D on validMaterials.modelKey = models3D.modelId order by modelKey")
            resultado = cursor.fetchall()
            if resultado != None:
                validList = []
                for registro in resultado:
                    validList.append({
                        "modelKey" : registro[0],
                        "modelName" : registro[1],
                        "modelImage" : registro[2],
                        "materialKey" : registro[3],
                        "materialName" : registro[4]})
                return validList
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()
        
    @classmethod
    def insertValidMaterial(self, db, valido):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select modelKey, materialKey from validMaterials where modelKey = %s and materialKey = %s", (valido.getModelKey(), valido.getMaterialKey()))
            consulta = cursor.fetchone()
            if consulta != None:
                return 1
            cursor.execute("insert into validMaterials (modelKey, materialKey) values (%s, %s)", (valido.getModelKey(), valido.getMaterialKey()))
            db.connection.commit()
            return 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()
    
    @classmethod
    def deleteValidMaterial(self, db, valido):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select modelKey, materialKey from validMaterials where modelKey = %s and materialKey = %s", (valido.getModelKey(), valido.getMaterialKey()))
            consulta = cursor.fetchone()
            if consulta == None:
                return 1
            else:
                cursor.execute("call deleteValidMaterial(%s, %s)", (valido.getModelKey(), valido.getMaterialKey()))
                db.connection.commit()
                return 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()