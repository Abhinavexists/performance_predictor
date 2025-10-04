import sys
from types import TracebackType
from typing import Optional

# def error_message_details(error, error_details:sys) -> here sys is just for type hinting 

# sys.exc_info()[2] can return either a TracebackType or None. 
# so type checkers complain because None is not allowed in the signature.
# Need to allow Optional[TracebackType] to handle both TraceBack and None

def error_message_details(error: Exception, error_details: Optional[TracebackType]) -> str:
    if error_details is None:
       error_details = sys.exc_info()[2]

    if error_details:
       file_name = error_details.tb_frame.f_code.co_filename
       line_no = error_details.tb_lineno
    else:
        file_name = 'Unknown'
        line_no = -1

    return "Error found in script [{0}] in line [{1}], Error message is [{2}]".format(file_name, line_no, str(error))

class CustomException(Exception):
    def __init__(self, error_message: Exception, error_detail: Optional[TracebackType]):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details=error_detail)

    def __str__(self) -> str:
        return self.error_message