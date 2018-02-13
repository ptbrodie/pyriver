import json

from pyriver.models import Event, joins


def create_event(river, event):
    model = Event()
    model.timestamp = event["metadata"]["timestamp"]
    model.value = json.dumps(event)
    river.events.append(model)
    river.save()


def get_events(river, page, start_date, end_date):
    return Event.query. \
        join(joins.river_event_join, (joins.river_event_join.c.event_id == Event.id)). \
        filter(joins.river_event_join.c.river_id == river.id). \
        order_by(Event.timestamp.desc()). \
        limit(100). \
        offset(100*page). \
        all()


def to_doc(event):
    return json.loads(event.value)["data"]
