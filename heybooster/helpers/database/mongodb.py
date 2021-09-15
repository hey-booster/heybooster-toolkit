import pymongo


class MongoDBHelper:
    """ MongoDB Helper"""

    def __init__(self, **kwargs):
        """
        Init Function
        :param kwargs:
        """
        self.client = pymongo.MongoClient(kwargs['uri'])
        self._database = getattr(self.client, kwargs['database'])

    def __enter__(self):
        """
        This function return self
        :return:
        """
        return self

    def __exit__(self, **kwargs):
        """
        This function connection close when context manager end
        :param kwargs:
        :return:
        """
        try:
            if self.client:
                self.client.close()
        except:
            pass

    @DeprecationWarning
    def insert(self, collection: str, data: dict) -> object:
        """
        This function insert data in collection
        :param collection:
        :param data:
        :return:object
        """
        return self._database[collection].insert(data)

    def insert_one(self, collection: str, data: dict) -> pymongo.InsertOne:
        """
        This function insert data in collection
        :param collection: str
        :param data: dict
        :return: pymongo.InsertOne
        """
        return self._database[collection].insert_one(data)

    def find_one(self, collection: str, query: dict, projection: dict = {}, default: object = None) -> dict:
        """
        This function get query result in collection
        :param collection: str
        :param query: dict
        :param projection: dict
        :return: dict
        """
        try:
            if bool(projection):
                return self._database[collection].find_one(query, projection)
            else:
                return self._database[collection].find_one(query)
        except Exception as e:
            if default:
                return default

            raise Exception(e)

    def find(self, collection: str, query: dict, projection: dict = {}, default: object = None) -> list:
        """
        This function list query results in collection
        :param collection: str
        :param query: dict
        :param projection: dict
        :param: default Object
        :return: list
        """
        try:
            if bool(projection):
                return self._database[collection].find(query, projection)
            else:
                return self._database[collection].find(query)
        except Exception as e:
            if default:
                return default

            raise Exception(e)

    def find_and_modify(self, collection: str, query: dict, default: object = None, **kwargs) -> list:
        """
        This function find and modify data in collection
        :param collection: 
        :param query: 
        :param kwargs: 
        :return: list
        """
        try:
            return self._database[collection].find_and_modify(
                query=query,
                update={"$set": kwargs},
                upsert=False,
                full_response=True
            )
        except Exception as e:
            if default:
                return default

            raise Exception(e)

    def close(self):
        """
        This function call __exit__ function for close mongo connection
        """
        return self.__exit__