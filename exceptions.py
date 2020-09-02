# Purpose:  Exceptions


class VeracodeError(Exception):
    """Raised when something goes wrong"""
    pass


class VeracodeAPIError(Exception):
    """Raised when something goes wrong with talking to the Veracode API"""
    pass
