
from enum import Enum


class ErrorEnum(Enum):
    """Enum for error codes."""

    # General
    SUCCESS = 0
    FAILURE = 1

    # File
    FILE_NOT_FOUND = 2
    FILE_NOT_READABLE = 3
    FILE_NOT_WRITABLE = 4

    # Directory
    DIRECTORY_NOT_FOUND = 5
    DIRECTORY_NOT_READABLE = 6
    DIRECTORY_NOT_WRITABLE = 7

    # Network
    NETWORK_ERROR = 8

    # Database
    DATABASE_ERROR = 9
    RECORD_NOT_FOUND = 13
    RECORD_ALREADY_EXISTS = 14

    #SERVICE
    USER_NOT_FOUND = 14
    USER_ALREADY_EXISTS = 15

    # Authentication
    INVALID_CREDENTIALS = 10

    #Validation
    SIGNATURE_HAS_EXPIRED = 11
    PASSWORD_NOT_FOUND = 12


    def __str__(self):
        return self.name



    