import mysql.connector as db

"""
MySQL Connection Helper
"""
class MySQLConnection:
    def __init__(self, host, port, user, password):
        self.__host = host
        self.__user = user
        self.__port = port
        self.__password = password
        self.__connection = None
        self.__cursor = None

    def __enter__(self):
        self.__connection = db.connect(
            host=self.__host,
            user=self.__user,
            port=self.__port,
            password=self.__password
        )
        self.__cursor = self.__connection.cursor(dictionary=True)
        return self.__cursor

    # our destructor
    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.__connection.rollback()
        else:
            self.__connection.commit()

        if self.__cursor:
            self.__cursor.close()
        if self.__connection:
            self.__connection.close()