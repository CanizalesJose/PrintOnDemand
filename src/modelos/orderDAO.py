from .order import order
from .model3D import Model3D

class orderDAO():
    @classmethod
    def getOrderWithUser(self, db, userName):
        try:
            cursor = db.connection.cursor()
            cursor.execute('select orderId, orderDate, orderTotalCost, orderUser, orderAddress from orders where orderUser = %s', (userName, ))
            resultado = cursor.fetchall()
            if resultado == ():
                return []
            else:
                pedidos = []
                for pedido in resultado:
                    newPedido = order(pedido[0], pedido[1], float(pedido[2]), pedido[3], pedido[4])
                    pedidos.append(newPedido)
                return pedidos
        except Exception as ex:
            raise Exception(ex)
        finally:
            db.connection.cursor().close()
    
    @classmethod
    def getModelsWithUser(self, db, username, orderId):
        try:
            cursor = db.connection.cursor()
            cursor.execute('select orderModelKey, orderModelFile, orderModelName, orderMaterialName, orderModelQty, orderModelPrice, round((orderModelQty*orderModelPrice*orderMaterialPriceModifier), 2) as subtotal from orders inner join ordermodels on orders.orderId = orderModels.orderKey where orderUser = %s and orderId = %s', (username, orderId))
            resultado = cursor.fetchall()
            if resultado == ():
                return []
            else:
                modelos = []
                for modelo in resultado:
                    newModelo = {
                        'modelKey' : modelo[0],
                        'modelFile' : modelo[1],
                        'modelName' : modelo[2],
                        'materialName' : modelo[3],
                        'modelQty' : modelo[4],
                        'modelPrice' : modelo[5],
                        'subtotal' : modelo[6]
                    }
                    modelos.append(newModelo)
                return modelos

        except Exception as ex:
            raise Exception(ex)
        finally:
            db.connection.cursor().close()
    
    @classmethod
    def getCustomModelsWithUser(self, db, username, orderId):
        try:
            cursor = db.connection.cursor()
            cursor.execute('select customModelId, customModelFile, customModelName, customMaterialName, customModelQty, customModelPrice, round((customModelQty*customModelPrice*customMaterialPriceModifier), 2) as subtotal from orders inner join customordermodels on orders.orderId = customorderModels.orderKey where orderUser =  %s and orderId = %s', (username, orderId))
            resultado = cursor.fetchall()
            if resultado == ():
                return []
            else:
                modelos = []
                for modelo in resultado:
                    newModelo = {
                        'modelKey' : modelo[0],
                        'modelFile' : modelo[1],
                        'modelName' : modelo[2],
                        'materialName' : modelo[3],
                        'modelQty' : modelo[4],
                        'modelPrice' : modelo[5],
                        'subtotal' : modelo[6]
                    }
                    modelos.append(newModelo)
                return modelos

        except Exception as ex:
            raise Exception(ex)
        finally:
            db.connection.cursor().close()

    @classmethod
    def getOrderFromId(self, db, orderId):
        try:
            cursor = db.connection.cursor()
            cursor.execute('select orderId, orderDate, orderTotalCost, orderUser, orderAddress from orders where orderId = %s', (orderId, ))
        except Exception as ex:
            raise Exception(ex)
        finally:
            db.connection.cursor().close()