import logging
import mysql.connector
from mysql.connector import Error

class DBConnection:
    __host=''
    __database=''
    __user=''
    __password=''

    def __init__(self, host, database, user, password):
        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password

    def get_host(self):
        return self.__host

    def get_database(self):
        return self.__database

    def get_user(self):
        return self.__user

    def get_password(self):
        return self.__password

    def set_host(self, host):
        self.__host = host

    def set_database(self, database):
        self.__database = database

    def set_user(self, user):
        self.__user = user

    def set_password(self, password):
        self.__password = password

    def executeQuery(self, c, q):
        logging.debug('Ejecutando sentencia ' + q)
        cursor = c.cursor()
        cursor.execute(q)
        tables = cursor.fetchall()
        logging.debug('Resultados: ' + str(tables))
        return tables

    def getMySQLConnection(self):
        logging.info('Estableciendo conexión con la base de datos...')
        try:
            connection = mysql.connector.connect(
                host=self.get_host(),
                database=self.get_database(),
                user=self.get_user(),
                password=self.get_password()
                )
            if connection.is_connected():
                db_Info = connection.get_server_info()
                logging.info("Connected to MySQL Server version" + str(db_Info))
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                logging.info("You're connected to database: " + str(record))
                return connection;
        except Error as e:
            logging.error("Error connecting to MySQL " + str(e))
            return

