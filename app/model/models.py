from typing import Union, Dict, List
from enum import Enum
from pydantic import BaseModel

class Status(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class APIResponse(BaseModel):
    status: Status
    message: Union[Dict, List[str], str]

def success_response(message: Union[Dict, List[str], str]) -> APIResponse:
    return APIResponse(status=Status.SUCCESS, message=message)

