class ClientException(Exception):
    pass


class ReportException(ClientException):
    pass


class EmptyLineError(ClientException):
    pass


class PendingDeprecationWarning(ClientException):
    pass
