import datetime
import typing
from fastapi import APIRouter
from common.schema import EventsList, Event, Status
from common.store import all_events
from common.exceptions import MyErrors, ApiException
from routers.utils import add_event_to_store, sort_events_dict, get_curr_date_from_id

router = APIRouter()


@router.get(path="/get_curr_date_events")
async def get_curr_date_events(curr_date: datetime.date) -> typing.List[Event]:
    """
    get_curr_date_events\n
    curr_date (Format : %Y-%m-%d)
    :
    """
    if curr_date not in all_events.all_events_dict:
        return []
    return sort_events_dict(all_events.all_events_dict[curr_date].events)


@router.post(path="/add_event")
async def add_event(event: Event):
    """
    add_event\n
    event name: (string) \n
    start time: (Format : %Y-%m-%dT%H:%M:%S) \n
    end time: (Format : %Y-%m-%dT%H:%M:%S) \n
    description: (string) (Optional)
    :
    """
    if event.start_time.date()!=event.end_time.date():
        raise ApiException(MyErrors.NO_DATE_SPILL[0], MyErrors.NO_DATE_SPILL[1])
    if event.start_time>=event.end_time:
        raise ApiException(MyErrors.WRONG_ORDER[0], MyErrors.WRONG_ORDER[1])
    
    status, reason, event_id = add_event_to_store(event)
    print(len(all_events.all_events_dict[event.start_time.date()].events))
    print(all_events.all_events_dict[event.start_time.date()].events)
    if not status:
        raise ApiException(status_code=530, error_msg=reason)
    return {"event_id": event_id}



@router.get(path="/delete_event")
async def delete_event(event_id: str):
    curr_date: datetime.date = get_curr_date_from_id(event_id=event_id)
    if curr_date in all_events.all_events_dict:
        try:
            del all_events.all_events_dict[curr_date].events[event_id]
            return {"event_id": event_id}
        except Exception as e:
            return ApiException(status_code=MyErrors.EVENT_ID_NOT_FOUND[0], error_msg=MyErrors.EVENT_ID_NOT_FOUND[1])
    else:
        return ApiException(status_code=MyErrors.EVENT_ID_NOT_FOUND[0], error_msg=MyErrors.EVENT_ID_NOT_FOUND[1])
   

@router.post(path="/update_event")
async def update_event(event_id: str, event: Event):
    if event.start_time.date()!=event.end_time.date():
        raise ApiException(MyErrors.NO_DATE_SPILL[0], MyErrors.NO_DATE_SPILL[1])
    if event.start_time>=event.end_time:
        raise ApiException(MyErrors.WRONG_ORDER[0], MyErrors.WRONG_ORDER[1])
    curr_date: datetime.date = get_curr_date_from_id(event_id=event_id)
    if curr_date!=event.start_time.date():
        raise ApiException(MyErrors.UPDATE_WITHIN_SAME_DATE[0], MyErrors.UPDATE_WITHIN_SAME_DATE[1])
    if curr_date in all_events.all_events_dict:
        try:
            event.event_id = all_events.all_events_dict[curr_date].events[event_id].event_id # event_id shouldn't be changed
            all_events.all_events_dict[curr_date].events[event_id] = event
            return {"event_id": event_id}
        except Exception as e:
            return ApiException(status_code=MyErrors.EVENT_ID_NOT_FOUND[0], error_msg=MyErrors.EVENT_ID_NOT_FOUND[1])
    else:
        return ApiException(status_code=MyErrors.EVENT_ID_NOT_FOUND[0], error_msg=MyErrors.EVENT_ID_NOT_FOUND[1])
    