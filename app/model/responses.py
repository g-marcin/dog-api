from typing import Optional
from pydantic import BaseModel


class DescriptionMessage(BaseModel):
    breed: str
    variant: Optional[str] = None
    description_en: str
    description_pl: str


class PerformanceMessage(BaseModel):
    cpu_usage: str
    memory_usage: str
    disk_usage: str
    thread_count: int
    uptime_seconds: float
