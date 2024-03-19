class material():
    def __init__(self, materialId: str, materialName: str, materialPriceModifier: float):
        self._materialId = materialId
        self._materialName = materialName
        self._materialPriceModifier = materialPriceModifier
    
    def getMaterialId(self) -> str:
        return self._materialId
    def setMaterialId(self, materialId) -> None:
        self._materialId = materialId
    
    def getMaterialName(self) -> str:
        return self._materialName
    def setMaterialName(self, materialName) -> None:
        self._materialName = materialName
    
    def getMaterialPriceModifier(self) -> float:
        return self._materialPriceModifier
    def setMaterialPriceModifier(self, materialPriceModifier) -> None:
        self._materialPriceModifier = materialPriceModifier