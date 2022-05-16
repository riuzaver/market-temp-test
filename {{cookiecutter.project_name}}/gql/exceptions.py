class BaseGqlException(ValueError):
    def __init__(self, message=None) -> None:
        if message is not None:
            self.message = message


class BadRequest(BaseGqlException):
    message = "Bad request"


class Forbidden(BaseGqlException):
    message = "Forbidden"
