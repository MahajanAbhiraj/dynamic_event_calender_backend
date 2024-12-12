from ast import List
import datetime
import typing
from common.store import all_events
from common.schema import Event, EventsList


def generate_id(curr_date: datetime.date) -> str:
    all_events.count = all_events.count + 1
    return f"{curr_date.year:04}{curr_date.month:02}{curr_date.day:02}{all_events.count:04}"

def get_curr_date_from_id(event_id: str) -> datetime.date:
    curr_date: datetime.date = datetime.datetime(year=int(event_id[0:4]), month=int(event_id[4:6]), day=int(event_id[6:8])).date()
    return curr_date


def add_event_to_store(curr_event: Event) -> typing.Tuple[bool, str, str | None]:
    start_time: datetime.datetime = curr_event.start_time
    end_time: datetime.datetime = curr_event.end_time
    curr_date: datetime.date = start_time.date()
    
    if curr_date not in all_events.all_events_dict:
        event_id: str = generate_id(curr_date)
        all_events.all_events_dict[curr_date] = EventsList(curr_date=curr_date, events={event_id: curr_event})
        return True, "Created new list of events for curr date", event_id
    
    for event_id, event_i in all_events.all_events_dict[curr_date].events.items():
        l, r = (event_i.start_time, event_i.end_time)
        if l<start_time:
            if r>start_time:
                return False, f"Overlapping with ({l}, {r})", None
        elif l==start_time:
            return False, "Same start time not allowed", None
        else:
            if l<end_time:
                return False, f"Overlapping with ({l}, {r})", None
            
    curr_event_id: str = generate_id(curr_date=curr_date)
    all_events.all_events_dict[curr_date].events[curr_event_id] = curr_event
    return True, "No overlapping events", curr_event_id

def sort_events_dict(events_dict: typing.Dict[str, Event]) -> typing.List[Event]:
    events: typing.List[Event] = []
    for i, val in events_dict.items():
        events.append(val)
    sorted_events = sorted(events, key=lambda x: x.start_time)
    print(sorted_events)
    return sorted_events


