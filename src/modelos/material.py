class material():
    def __init__(self, materialId, materialName, materialPriceModifier) -> None:
        self._materialId = materialId
        self._materialName = materialName
        self._materialPriceModifier = materialPriceModifier
    
    def getMaterialId(self):
        return self._materialId
    def setMaterialId(self, materialId):
        self._materialId = materialId
    
    def getMaterialName(self):
        return self._materialName
    def setMaterialName(self, materialName):
        self._materialName = materialName
    
    def getMaterialPriceModifier(self):
        return self._materialPriceModifier
    def setMaterialPriceModifier(self, materialPriceModifier):
        self._materialPriceModifier = materialPriceModifier