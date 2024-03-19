class userType:
    def __init__(self, userTypeId: int, userTypeName: str):
        self._userTypeId = userTypeId
        self._userTypeName = userTypeName
    
    def getUserTypeId(self) -> int:
        return self._userTypeId
    def setUserTypeId(self, newUserTypeId) -> None:
        self._userTypeId = newUserTypeId

    def getUserTypeName(self) -> str:
        return self._userTypeName
    def setUserTypeName(self, newUserTypeName) -> None:
        self._userTypeName = newUserTypeName