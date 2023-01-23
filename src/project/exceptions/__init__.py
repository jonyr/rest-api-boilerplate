from werkzeug.exceptions import HTTPException


class CustomException(HTTPException):
    def __init__(self, message: str = "Bad request", code: str = "BadRequestError", status_code: int = 400):
        super().__init__()

        self.code = code
        self.message = message
        self.status_code = status_code
