from pydantic import BaseModel
import datetime
import typing

class Event(BaseModel):
    event_id: str | None = None
    event_name: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    description: str | None = None

class EventsList(BaseModel):
    curr_date: datetime.date
    events: dict[str, Event]

class AllEvents:
    def __init__(self, all_events_dict: typing.Dict[datetime.date, EventsList] = {}) -> None:
        self.all_events_dict = all_events_dict
        self.count: int = 0

class Status(BaseModel):
    status: str
    reason: str | None = None
    event_id: str | None = None
    
    