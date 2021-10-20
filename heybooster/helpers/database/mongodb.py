import pymongo
from pymongo.command_cursor import CommandCursor


class MongoDBHelper:
    """ MongoDB Helper"""

    def __init__(self, **kwargs):
        """
        Init Function
        :param kwargs:
        :return:
        """
        self.client = pymongo.MongoClient(kwargs['uri'])
        self._database = getattr(self.client, kwargs['database'])

    def __enter__(self):
        """
        This function return self
        :return:
        """
        return self

    def __exit__(self, *args, **kwargs):
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

    def find_one(self, collection: str, query: dict, projection: dict = {}, default: object = None, **kwargs) -> dict:
        """
        This function get query result in collection
        :param collection: str
        :param query: dict
        :param projection: dict
        :return: dict
        """
        try:
            if bool(projection):
                return self._database[collection].find_one(query, projection, **kwargs)
            else:
                return self._database[collection].find_one(query, **kwargs)
        except Exception as e:
            if default:
                return default

            raise Exception(e)

    def find(self, collection: str, query: dict, projection: dict = {}, default: object = None, **kwargs) -> list:
        """
        This function list query results in collection
        :param collection: str
        :param query: dict
        :param projection: dict
        :param: default: Object
        :return: list
        """
        try:
            if bool(projection):
                return self._database[collection].find(query, projection, **kwargs)
            else:
                return self._database[collection].find(query, **kwargs)
        except Exception as e:
            if default:
                return default

            raise Exception(e)

    def find_and_modify(self, collection: str, query: dict, **kwargs) -> list:
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
            raise Exception(e)

    def aggregate(self, collection: str, pipeline: list, options: dict = {}, default: object = None) -> CommandCursor:
        """
        This function aggregations in mongodb
        :param collection:
        :param pipeline:
        :param options:
        :param default:
        :return object:
        """
        try:
            if bool(options):
                return self._database[collection].aggregate(pipeline, options)
            else:
                return self._database[collection].aggregate(pipeline)
        except Exception as e:
            if default:
                return default
            raise Exception(e)

    def remove(self, collection: str, query: dict):
        """
        This function delete data in collection
        :param collection:
        :param query:
        :return:object
        """
        try:
            self._database[collection].remove(query)
        except Exception as e:
            raise Exception(e)

    def delete_many(self, collection: str, query: dict):
        """
        This function delete many data in collection
        :param collection:
        :param query:
        :return:object
        """
        try:
            self._database[collection].delete_many(query)
        except Exception as e:
            raise Exception(e)

    def delete_one(self, collection: str, query: dict):
        """
        This function delete data in collection
        :param collection:
        :param query:
        :return:object
        """
        try:
            self._database[collection].delete_one(query)
        except Exception as e:
            raise Exception(e)

    def update(self, collection: str, query: dict, update: dict) -> object:
        """
        This function update data in collection
        :param collection:
        :param query:
        :param update:
        :return:object
        """
        try:
            return self._database[collection].update(query, update)
        except Exception as e:
            raise Exception(e)

    def update_many(self, collection: str, query: dict, update: dict) -> object:
        """
        This function update many data in collection
        :param collection:
        :param query:
        :param update:
        :return:object
        """
        try:
            return self._database[collection].update_many(query, update)
        except Exception as e:
            raise Exception(e)

    def close(self):
        """
        This function call __exit__ function for close mongo connection
        """
        return self.__exit__
