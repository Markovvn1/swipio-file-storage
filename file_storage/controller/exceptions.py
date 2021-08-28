class ControllerException(Exception):
    pass


class FileControllerException(ControllerException):
    """File corrupted"""


class CorruptedFileControllerException(FileControllerException):
    """File corrupted"""
