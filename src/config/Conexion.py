import MySQLdb
from config.config import DevelopmentConfig

class Conexion():
    @classmethod
    def generarConexion(self):
        try:
            db = MySQLdb.connect(host=DevelopmentConfig.MYSQL_HOST, user=DevelopmentConfig.MYSQL_USER, password=DevelopmentConfig.MYSQL_PASSWORD, db=DevelopmentConfig.MYSQL_DB)
            return db
        except Exception as ex:
            raise Exception(ex)
