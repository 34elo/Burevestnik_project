class ClientException(Exception):
    pass

class ReportException(ClientException):
    pass

class EmptyLineError(ClientException):
    pass