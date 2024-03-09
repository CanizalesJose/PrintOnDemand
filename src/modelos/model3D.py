
class Model3D:

    def __init__(self, modelId, modelName, modelImage, modelFile, modelBasePrice):
        self._modelId = modelId
        self._modelName = modelName
        self._modelImage = modelImage
        self._modelFile = modelFile
        self._modelBasePrice = modelBasePrice

    def getModelId(self):
        return self._modelId

    def setModelId(self, newModelId):
        self._modelId = newModelId

    def getModelName(self):
        return self._modelName
    
    def setModelName(self, newModelName):
        self._modelName = newModelName

    def getModelImage(self):
        return self._modelImage

    def setModelImage(self, newModelImage):
        self._modelImage = newModelImage

    def getModelFile(self):
        return self._modelFile

    def setModelFile(self, newModelFile):
        self._modelFile = newModelFile
    
    def getModelBasePrice(self):
        return self._modelBasePrice

    def setModelBasePrice(self, newModelBasePrice):
        self._modelBasePrice = newModelBasePrice