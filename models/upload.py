from enum import Enum

from pydantic import BaseModel


class UploadStatus(str, Enum):
    complete = "COMPLETE"
    in_progress = "IN_PROGRESS"
    error = "ERROR"


class UploadOut(BaseModel):
    status: UploadStatus
