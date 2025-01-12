from pydantic import BaseModel


class SetPlayPresenceSchemas(BaseModel):
    title: str
    author: str
    cover: str
    start_timestamp: int | float | None
    pause_timestamp: int | float | None
    duration: int | float
    new: bool


class SetPausePresenceSchemas(BaseModel):
    title: str
    author: str
    cover: str
