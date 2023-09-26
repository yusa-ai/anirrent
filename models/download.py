from enum import Enum

from pydantic import UUID4, BaseModel


class DownloadStatus(str, Enum):
    complete = "COMPLETE"
    in_progress = "IN_PROGRESS"
    error = "ERROR"


class DownloadIn(BaseModel):
    magnet_url: str
    entry_name: str
    season: int | None = None
    episode: int | None = None


class DownloadOut(BaseModel):
    download_uuid: UUID4
    progress: float
    status: DownloadStatus


class DownloadUUID(BaseModel):
    download_uuid: UUID4
