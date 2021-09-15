from enum import Enum

class HTTPMethods(Enum):
    delete = 0
    get = 1
    post = 2
    put = 3


class AuthenticationError(Exception):
    pass


class CredentialsError(Exception):
    pass


class UnhandledResponseError(Exception):
    pass
