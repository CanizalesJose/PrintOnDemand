from .material import material

class materialDAO():
    @classmethod
    def getAllMaterials(self, db):
        cursor = db.connection.cursor()
        cursor.execute("select materialId, materialName, materialPriceModifier from materials")
        resultados = cursor.fetchall()
        if resultados == ():
            return None
        materialsList = []
        for registro in resultados:
            materialsList.append(material(registro[0], registro[1], registro[2]))
        return materialsList
    
    @classmethod
    def insertMaterial(self, db, newMaterial):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select materialId from materials where materialId = %s", (newMaterial.getMaterialId(),))
            consulta = cursor.fetchone()
            if consulta != None:
                return 1
            cursor.execute("insert into materials values (%s, %s, %s)", (newMaterial.getMaterialId(), newMaterial.getMaterialName(), float(newMaterial.getMaterialPriceModifier())))
            db.connection.commit()
            return 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def updateMaterial(self, db, material):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select materialId from materials where materialId = %s", (material.getMaterialId(),))
            consulta = cursor.fetchone()
            if consulta == None:
                return 1
            else:
                cursor.execute("update materials set materialName = %s, materialPriceModifier = %s where materialId = %s", (material.getMaterialName(), float(material.getMaterialPriceModifier()), material.getMaterialId()))
                db.connection.commit()
                return 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()
    
    @classmethod
    def deleteMaterial(self, db, materialId):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select materialId from materials where materialId = %s", (materialId, ))
            consulta = cursor.fetchone()
            if consulta == None:
                return 1
            else:
                cursor.execute("call deleteMaterial(%s)", (materialId, ))
                db.connection.commit()
                return 0
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            cursor.close()
        
    @classmethod
    def getMaterialData(self, db, materialId):
        try:
            cursor = db.connection.cursor()
            cursor.execute("select materialName, materialPriceModifier from materials where materialId = %s", (materialId, ))
            consulta = cursor.fetchone()
            if consulta == None:
                return 1
            else:
                return material(materialId, consulta[0], consulta[1])
        except Exception as ex:
            raise Exception(ex)
        finally:
            db.connection.cursor().close()