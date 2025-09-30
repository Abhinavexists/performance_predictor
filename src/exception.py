import sys
from types import TracebackType
from typing import Optional

# def error_message_details(error, error_details:sys) -> here sys is just for type hinting 

# sys.exc_info()[2] can return either a TracebackType or None. 
# so type checkers complain because None is not allowed in the signature.
# Need to allow Optional[TracebackType] to handle both TraceBack and None

tb = sys.exc_info()[2]

def error_message_details(error: Exception, error_details: Optional[TracebackType] = tb) -> str:
    file_name = error_details.tb_frame.f_code.co_filename if error_details else None
    line_no = error_details.tb_lineno if error_details else None

    error_message = "Error found in script [{0}] in line [{1}], Error message is [{2}]".format(file_name, line_no, str(error))
    return error_message

class CustomException(Exception):
    def __init__(self, error_message: Exception, error_detail: Optional[TracebackType] = tb):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details=error_detail)

    def __str__(self) -> str:
        return self.error_message