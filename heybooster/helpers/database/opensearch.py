import requests
from requests.auth import HTTPBasicAuth


class OpenSearchHelper:
    """ OpenSearch (ElasticSearch) Helper """
    GET = "get"
    PUT = "put"
    POST = "post"

    def __init__(self, url: str, index: str, username: str = None, password: str = None):
        self.url = url
        self.index = index
        self.auth = None
        self.username = username
        self.password = password

        if all([username, password]):
            self.__set_auth()

        self.__check_url()

    def get_url(self, path: str) -> str:
        """ This function return url with given path """
        return f"{self.url}/{self.index}/{path}"

    def __perform_request(self, method: str, url: str, payload: dict = {}, expected_status: int = 200) -> dict:
        """
        This function send request and check expected status after return respose
        """
        response = requests.request(
            method=method,
            url=url,
            auth=self.auth,
            headers={
                "Content-Type": "application/json"
            },
            json=payload
        )

        if response.status_code != expected_status:
            raise Exception(f"Reponse Status Code -> {response.status_code} \n Message -> {response.text}")

        return response.json()

    def __set_auth(self):
        """
        This function set request authentication
        """
        self.auth = HTTPBasicAuth(username=self.username, password=self.password)

    def __check_url(self):
        """
        This function check url is working
        """
        try:
            response = self.__perform_request(method=OpenSearchHelper.GET, url=self.get_url(path="_search"))

            if not response:
                raise BaseException("URL Not Working")

        except Exception as exception:
            raise Exception(exception)

    def update_or_insert(self, data: dict, _id: str = None) -> dict:
        """
        This function insert data or update date (if has _id)
        """
        try:
            response = self.__perform_request(
                method=OpenSearchHelper.POST,
                url=self.get_url(path="_doc" if not _id else f"_doc/{_id}"),
                payload=data,
                expected_status=200 if _id else 201
            )

            return response
        except Exception as exception:
            raise Exception(exception)

    def search(self, size: int = 10, sort: str = "_id:desc", **kwargs):
        """
        This function returns search response
        """
        try:
            path = f"_search"
            url = self.get_url(path=path)
            sort_key = sort.split(":")[0]
            sort_order = sort.split(":")[1]

            payload = {
                "sort": [
                    {
                        sort_key: {
                            "order": sort_order
                        }
                    }
                ],
                "size": size,
                "query": {
                    "match": {
                        **kwargs
                    }
                }
            }

            response = self.__perform_request(
                method=OpenSearchHelper.GET,
                url=url,
                payload=payload,
            )

            return response
        except Exception as exception:
            raise Exception(exception)

    def get(self, payload: dict = {}):
        """
        This function is return data for payload
        """
        try:
            return requests.get(url=self.get_url(path="_search"), json=payload, auth=self.auth)
        except Exception as e:
            raise Exception(e)
