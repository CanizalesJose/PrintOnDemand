class validMaterial():
    def __init__(self, modelKey, materialKey):
        self._modelKey = modelKey
        self._materialKey = materialKey

    def getModelKey(self):
        return self._modelKey
    def setModelKey(self, modelKey):
        self._modelKey = modelKey

    def getMaterialKey(self):
        return self._materialKey
    def setMaterialKey(self, materialKey):
        self._materialKey = materialKey