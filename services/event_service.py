import json

from client.models import Event


def create_event(river, event):
    model = Event()
    model.timestamp = event["metadata"]["timestamp"]
    model.value = json.dumps(event)
    river.events.append(model)
    river.save()

