# Purpose:  Exceptions


class VeracodeError(Exception):
    def __init__(self, message): 
        super().__init__(message)
    """Raised when something goes wrong"""
    pass


class VeracodeAPIError(Exception):
    def __init__(self, message): 
        super().__init__(message)
    """Raised when something goes wrong with talking to the Veracode API"""
    pass
