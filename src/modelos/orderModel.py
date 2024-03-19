class orderModel:
    def __init__(self, isCustom: bool, modelKey: str, modelName: str, modelFile: str, modelPrice: float, modelQty: int, materialKey: str, materialName: str, materialPriceModifier: float)  -> None:
        self._isCustom = isCustom
        self._modelKey = modelKey
        self._modelName = modelName
        self._modelFile = modelFile
        self._modelPrice = modelPrice
        self._modelQty = modelQty
        self._materialKey = materialKey
        self._materialName = materialName
        self._materialPriceModifier = materialPriceModifier
    
    def getIsCustom(self):
        return self._isCustom
    def setIsCustom(self, isCustom: bool):
        self._isCustom = isCustom

    def getModelKey(self) -> str:
        return self._modelKey
    def setModelKey(self, modelKey: str) -> None:
        self._modelKey = modelKey

    def getModelName(self) -> str:
        return self._modelName
    def setModelName(self, modelName: str) -> None:
        self._modelName = modelName

    def getModelFile(self) -> str:
        return self._modelFile
    def setModelFile(self, modelFile: str) -> None:
        self._modelFile = modelFile

    def getModelPrice(self) -> float:
        return self._modelPrice
    def setModelPrice(self, modelPrice: float) -> None:
        self._modelPrice = modelPrice

    def getModelQty(self) -> int:
        return self._modelQty
    def setModelQty(self, modelQty: int) -> None:
        self._modelQty = modelQty

    def getMaterialKey(self) -> str:
        return self._materialKey
    def setMaterialKey(self, materialKey: str) -> None:
        self._materialKey = materialKey

    def getMaterialName(self) -> str:
        return self._materialName
    def setMaterialName(self, materialName: str) -> None:
        self._materialName = materialName

    def getMaterialPriceModifier(self) -> float:
        return self._materialPriceModifier
    def setMaterialPriceModifier(self, materialPriceModifier: float) -> None:
        self._materialPriceModifier = materialPriceModifier

    def toDict(self) -> dict:
        return {
            "isCustom": self._isCustom,
            "modelKey": self._modelKey,
            "modelName": self._modelName,
            "modelFile": self._modelFile,
            "modelPrice": self._modelPrice,
            "modelQty": self._modelQty,
            "materialKey": self._materialKey,
            "materialName": self._materialName,
            "materialPriceModifier": self._materialPriceModifier
        }