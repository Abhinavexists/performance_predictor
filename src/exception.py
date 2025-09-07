# import sys
from types import TracebackType

# def error_message_details(error, error_details:sys) -> here sys is just for type hinting 

def error_message_details(error: Exception, error_details: TracebackType) -> str:
    file_name = error_details.tb_frame.f_code.co_filename if error_details else None
    line_no = error_details.tb_lineno if error_details else None

    error_message = "Error found in script [{0}] in line [{1}], Error message is [{2}]".format(file_name, line_no, str(error))
    return error_message

class CustomException(Exception):
    def __init__(self, error_message: Exception, error_detail: TracebackType):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details=error_detail)

    def __str__(self) -> str:
        return self.error_message