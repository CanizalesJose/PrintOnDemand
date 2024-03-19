class Model3D:

    def __init__(self, modelId: str, modelName: str, modelImage: str, modelFile: str, modelBasePrice: float):
        self._modelId = modelId
        self._modelName = modelName
        self._modelImage = modelImage
        self._modelFile = modelFile
        self._modelBasePrice = modelBasePrice

    def getModelId(self) -> str:
        return self._modelId
    def setModelId(self, newModelId) -> None:
        self._modelId = newModelId

    def getModelName(self) -> str:
        return self._modelName
    def setModelName(self, newModelName) -> None:
        self._modelName = newModelName

    def getModelImage(self) -> str:
        return self._modelImage
    def setModelImage(self, newModelImage) -> None:
        self._modelImage = newModelImage

    def getModelFile(self) -> str:
        return self._modelFile
    def setModelFile(self, newModelFile) -> None:
        self._modelFile = newModelFile
    
    def getModelBasePrice(self) -> float:
        return self._modelBasePrice
    def setModelBasePrice(self, newModelBasePrice) -> None:
        self._modelBasePrice = newModelBasePrice