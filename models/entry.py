from enum import Enum

from pydantic import UUID4, BaseModel


class EntryType(str, Enum):
    tv = "TV"
    movie = "MOVIE"


class EntryIn(BaseModel):
    entry_name: str
    entry_type: EntryType


class EntryOut(BaseModel):
    entry_uuid: UUID4
    entry_name: str
    entry_type: EntryType
