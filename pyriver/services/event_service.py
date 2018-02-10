import json

from pyriver.models import Event


def create_event(river, event):
    model = Event()
    model.timestamp = event["metadata"]["timestamp"]
    model.value = json.dumps(event)
    river.events.append(model)
    river.save()


def get_events(river, page, start_date, end_date):
    return Event.query.filter_by(river_id=river.id).limit(100).offset(100*page)
