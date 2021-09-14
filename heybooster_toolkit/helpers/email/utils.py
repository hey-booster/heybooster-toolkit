from enum import Enum

class HTTPMethods(Enum):
    DELETE = 0
    GET = 1
    POST = 2
    PUT = 3


class AuthenticationError(Exception):
    pass


class CredentialsError(Exception):
    pass


class InvalidResponseError(Exception):
    pass


class RetryLimitExceededError(Exception):
    pass