from enum import Enum

class HTTPMethods(Enum):
    delete = 0
    get = 1
    post = 2
    put = 3


class AuthenticationError(Exception):
    def __str__(self) -> str:
        return 'Your credentials invalid. Check your credentials.'


class SendProcessFailureError(Exception):
    def __str__(self) -> str:
        return 'Email sending procedure failed.'
