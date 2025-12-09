import sys
from types import TracebackType
from typing import Optional

# def error_message_details(error, error_detail:sys) -> here sys is just for type hinting 

# sys.exc_info()[2] can return either a TracebackType or None. 
# so type checkers complain because None is not allowed in the signature.
# Need to allow Optional[TracebackType] to handle both TraceBack and None

def error_message_details(error: Exception, error_detail: Optional[TracebackType]) -> str:
    if error_detail is None:
       error_detail = sys.exc_info()[2]

    if error_detail is not None:
       file_name = error_detail.tb_frame.f_code.co_filename
       line_no = error_detail.tb_lineno
    else:
        file_name = 'Unknown'
        line_no = -1

    return f"Error found in script [{file_name}] in line [{line_no}], Error message is [{str(error)}]"

class CustomException(Exception):
    def __init__(self, error: Exception, error_detail: Optional[TracebackType] = None):
        super().__init__(error)
        self.error_message = error_message_details(error, error_detail=error_detail)

    def __str__(self) -> str:
        return self.error_message