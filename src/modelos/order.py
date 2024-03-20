class order:
    def __init__(self, orderId : str, orderDate : str, orderTotalCost : float, orderUser, orderAddress : str):
        self._orderId = orderId
        self._orderDate = orderDate
        self._orderTotalCost = orderTotalCost
        self._orderUser = orderUser
        self._orderAddress = orderAddress
    
    def getOrderId(self):
        return self._orderId
    def setOrderId(self, orderId):
        self._orderId = orderId

    def getOrderDate(self):
        return self._orderDate
    def setOrderDate(self, orderDate):
        self._orderDate = orderDate
    
    def getOrderTotalCost(self):
        return self._orderTotalCost
    def setOrderTotalCost(self, orderTotalCost):
        self._orderTotalCost = orderTotalCost

    def getOrderUser(self):
        return self._orderUser
    def setOrderUser(self, orderUser):
        self._orderUser = orderUser

    def getOrderAddress(self):
        return self._orderAddress
    def setOrderAddress(self, orderAddress):
        self._orderAddress = orderAddress