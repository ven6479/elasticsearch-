from pydantic import BaseModel
from typing import Optional


class Log(BaseModel):
    timestamp: str
    method: str
    path: str
    query_params: Optional[dict]
    status_code: Optional[int]
    response: Optional[dict]
    response_time: Optional[float]


