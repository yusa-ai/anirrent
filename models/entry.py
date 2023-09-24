from pydantic import BaseModel
from pydantic import UUID4
from enum import Enum


class EntryType(str, Enum):
    tv = "TV"
    movie = "MOVIE"


class Entry(BaseModel):
    entry_uuid: UUID4
    entry_name: str
    entry_type: EntryType
