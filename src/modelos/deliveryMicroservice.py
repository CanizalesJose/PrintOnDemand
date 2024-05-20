import MySQLdb

class deliveryMicroservice:

    @classmethod
    def generarConexionMicroservicio(self):
        try:
            db = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="deliverydb")
            return db
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def insertDeliveryUser(self, orderKey, orderDate, orderTotalQty, orderUser, orderAddress):
        try:
            db = self.generarConexionMicroservicio()
            cursor = db.cursor()
            cursor.execute("call addDeliveryWithUser(%s, %s, %s, %s, %s)", (orderKey, orderDate, orderTotalQty, orderUser, orderAddress))
            db.commit()
            cursor.close()
            return 0
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def insertDeliveryNoUser(self, orderKey, orderDate, orderTotalQty, orderAddress):
        try:
            db = self.generarConexionMicroservicio()
            cursor = db.cursor()
            cursor.execute("call addDeliveryNoUser(%s, %s, %s, %s)", (orderKey, orderDate, orderTotalQty, orderAddress))
            db.commit()
            cursor.close()
            return 0
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def showDeliveryStatus(self, orderKey):
        statusHTML = ""
        try:
            db = self.generarConexionMicroservicio()
            cursor = db.cursor()
            cursor.execute("select statusId, statusDescription from delivery inner join validstatus on validstatus.statusId=delivery.orderstatus where orderKey=%s", (orderKey, ))
            registro = cursor.fetchone()
            if registro[0] != None:
                statusHTML += f'<h6 class="text-start"> Estado del envío: {registro[0]} - {registro[1]}</h6>'
                statusHTML += '<hr>'
                print("Se encontró pedido desde microservicio")
            cursor.close()
        except Exception as ex:
            raise Exception(ex)
        return statusHTML