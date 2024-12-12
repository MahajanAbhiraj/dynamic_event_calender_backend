from fastapi import HTTPException

class ApiException(HTTPException):
    def __init__(self, status_code: int, error_msg: str):
        super().__init__(status_code=status_code, detail=error_msg)


class MyErrors:
    NO_DATE_SPILL = (523, "Start time and end time should be present in same date")
    WRONG_ORDER = (524, "Start time should come before end time")
    UPDATE_WITHIN_SAME_DATE = (525, "Update within same date")
    OVERLAPPING_INTERVALS = (526, "")
    EVENT_ID_NOT_FOUND = (527, "Event ID not found")
    
