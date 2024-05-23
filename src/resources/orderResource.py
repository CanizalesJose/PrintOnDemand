from flask_restful import Resource
from config.Conexion import Conexion
import json

class orderResource(Resource):
    def get(self):
        try:
            db = Conexion.generarConexion()
            cursor = db.cursor()
            cursor.execute("select orderid, orderuser, ordermodelname, ordermodelprice, ordermodelqty, ordermaterialpricemodifier, ROUND((ordermodelprice*ordermodelqty*ordermaterialpricemodifier), 2) as total from ordermodels inner join orders on orders.orderid=ordermodels.orderkey order by orderid")
            resultados = cursor.fetchall()
        except Exception as ex:
            return {"error": str(ex)}, 500
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

        listaModelos = []
        for orden in resultados:
            newOrderModel = {
                'orderid' : orden[0],
                'orderuser' : orden[1],
                'ordermodelname' : orden[2],
                'ordermodelprice' : orden[3],
                'ordermodelqty' : orden[4],
                'ordermaterialpricemodifier' : orden[5],
                'total' : orden[6]
            }
            listaModelos.append(newOrderModel)
        return json.dumps(listaModelos), 200