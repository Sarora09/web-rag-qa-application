import traceback

class CustomException(Exception):
    def __init__(self, error_message, error_details = None, file_name=None, line_no=None):
        super().__init__(error_message)
        self.error_message = error_message
        if error_details is not None:
            exc_type, exc_value, exc_tb = error_details
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.line_no = exc_tb.tb_lineno
            self.trace = ''.join(traceback.format_tb(exc_tb))
        else:
            self.file_name = file_name
            self.line_no = line_no
            self.trace = None

    def __str__(self):
        return f"Error in {self.file_name} at line {self.line_no}. Error message: {self.error_message}."
    
    def __repr__(self):
        return f"CustomException({self.error_message!r}, file_name={self.file_name!r}, line_no={self.line_no})"