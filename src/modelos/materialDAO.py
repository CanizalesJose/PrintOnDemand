from .material import material

class materialDAO():
    @classmethod
    def getAllMaterials(self, db):
        cursor = db.connection.cursor()
        cursor.execute("select materialId, materialName, materialPriceModifier from materials")
        resultados = cursor.fetchall()
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