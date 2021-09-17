"""Database Helper"""
import os
import sys
import logging
import psycopg2
import psycopg2.extras
import psycopg2.extensions as psy_ext

logger = logging.getLogger(__name__)


class DBHelper:
    """
    This class context manager to db process
    """

    def __init__(self, **kwargs: dict):
        """
        Init Function
        :param user: required
        :param password: required
        :param host: required
        :param database: reuired
        :param port: optional default 5432
        """
        try:

            self._connection = psycopg2.connect(
                user=kwargs.get("user"),
                password=kwargs.get("password"),
                host=kwargs.get("host"),
                database=kwargs.get("database"),
                port=kwargs.get("port", 5432)
            )
            self._cursor = self._connection.cursor()
            self._connection.autocommit = kwargs.pop("auto_commit", True)
            self.last_execute = False

        except psycopg2.OperationalError as e:
            raise Exception("*Operational* Error: {}".format(e))

        except Exception as e:
            raise Exception("*Exception* Error: {}".format(e))

    def return_as_dict(self):
        """
        This Function Set Cursor Factory RealDictCursor
        :return:
        """
        self._cursor.close()
        self._cursor = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        return self

    def cursor(self) -> psy_ext.cursor:
        """
        This function return connection
        :return: Postgre Connection
        """
        return self._cursor

    def connection(self) -> psy_ext.connection:
        """
        This function return connection
        :return: Postgre Connection
        """
        return self._connection

    def __enter__(self):
        """
        This function return DBHelper
        :return: DBHelper
        """
        return self

    def __exit__(self, *args, **kwargs):
        """ This function will close connection and cursor if connection is open """
        if self._connection:
            self._cursor.close()
            self._connection.close()

    def execute(self, sql: str, params: tuple = ()) -> bool:
        """ This function execute sql query with params """
        try:
            self._cursor.execute(sql, params)
            self.last_execute = True

            return True
        except Exception as e:
            logger.error(e)
            self.last_execute = False

        return False

    def fetchall(self) -> list:
        """ This function return sql queries result """
        try:
            if self.last_execute:
                return self._cursor.fetchall()

            logger.info("Before calling the function, a successful SQL execution is required.")
        except Exception as e:
            logger.error("Error: {}".format(e))

        return []

    def fetchone(self) -> dict:
        """ This function return sql queries result """
        try:
            if self.last_execute:
                return self._cursor.fetchone()

            logger.info("Before calling the function, a successful SQL execution is required.")
        except Exception as e:
            logger.error("Error: {}".format(e))

        return {}
