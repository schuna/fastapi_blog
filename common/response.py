from typing import Any


class CustomResponse:
    def __init__(self, data: Any = None, success: bool = True, message: str = ""):
        self.data = data
        self.success = success
        self.message = message
