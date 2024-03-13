class userType:
    def __init__(self, userTypeId, userTypeName) -> None:
        self._userTypeId = userTypeId
        self._userTypeName = userTypeName
    
    def getUserTypeId(self):
        return self._userTypeId
    def setUserTypeId(self, newUserTypeId):
        self._userTypeId = newUserTypeId

    def getUserTypeName(self):
        return self._userTypeName
    def setUserTypeName(self, newUserTypeName):
        self._userTypeName = newUserTypeName