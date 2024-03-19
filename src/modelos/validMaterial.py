class validMaterial():
    def __init__(self, modelKey: str, materialKey: str):
        self._modelKey = modelKey
        self._materialKey = materialKey

    def getModelKey(self) -> str:
        return self._modelKey
    def setModelKey(self, modelKey) -> None:
        self._modelKey = modelKey

    def getMaterialKey(self) -> str:
        return self._materialKey
    def setMaterialKey(self, materialKey) -> None:
        self._materialKey = materialKey