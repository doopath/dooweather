"""
    Exceptions for this project.
"""


class InvalidTemperatureFormatException(Exception):
    pass


class CacheSessionIsNotStartedException(Exception):
    pass


class CacheSessionIsAlreadyStartedException(Exception):
    pass
