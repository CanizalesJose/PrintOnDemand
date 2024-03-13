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