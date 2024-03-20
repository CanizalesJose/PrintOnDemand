from .orderModel import orderModel
import secrets
from datetime import datetime

class orderModelDAO():
    
    @classmethod
    def confirmOrder(self, db, carrito, username, address):
        try:
            cursor = db.connection.cursor()
            # GENERA UN ID DE PEDIDO UNICO
            orderId = secrets.token_urlsafe()[:15]
            fechaActual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            total = 0

            cursor.execute("select orderId from orders where orderId = %s", (orderId, ))
            resultado = cursor.fetchone()
            while resultado != None:
                orderId = secrets.token_urlsafe()[:15]
                cursor.execute("select orderId from orders where orderId = %s", (orderId, ))
                resultado = cursor.fetchone()
            
            # CALCULAR TOTAL
            for registro in carrito:
                total += int(registro['modelQty'])*float(registro['modelPrice'])*float(registro['materialPriceModifier'])

            if username != None:
                cursor.execute("call insertOrderWithUser(%s, %s, %s, %s, %s)", (orderId, fechaActual, total, username, address))
            else:
                cursor.execute("call insertOrderNoUser(%s, %s, %s, %s)", (orderId, fechaActual, total, address))
            
            for registro in carrito:
                if registro['isCustom'] == False:
                    cursor.execute("call insertModelOrder(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (orderId, registro['modelKey'], registro['modelName'], registro['modelFile'], registro['modelPrice'], registro['modelQty'], registro['materialKey'], registro['materialName'], registro['materialPriceModifier']))
                else:
                    cursor.execute("call insertCustomModelOrder(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (orderId, registro['modelKey'], registro['modelName'], registro['modelFile'], registro['modelPrice'], registro['modelQty'], registro['materialKey'], registro['materialName'], registro['materialPriceModifier']))
            
            db.connection.commit()
            return orderId

        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
        finally:
            db.connection.cursor().close()