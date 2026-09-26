from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Status(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class APIResponse(BaseModel, Generic[T]):
    status: Status
    message: T


def success_response(message: T) -> APIResponse[T]:
    return APIResponse(status=Status.SUCCESS, message=message)
