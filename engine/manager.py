from time import time
import json

import redis

from client.engine.listener import Listener
from client.engine.processor import RiverProcessor
from client.services import RiverService
from client.services import event_service as events


class EventManager(object):

    def __init__(self):
        self.processors = []
        self.publisher = redis.Redis()
        self.aggregator = {}

    def init(self, schema):
        self.river = RiverService.create(schema)
        self.schema = schema
        self.initialized = True

    def run(self):
        raise NotImplementedError()

    def handle(self, channel=None, input=None):
        timestamp = int(time())
        if input:
            timestamp = input["metadata"]["timestamp"]
        self.before_processing()
        ievent = self.stage_input(channel, input)
        result = self.process(ievent)
        oevent = self.structure_output(timestamp, result)
        self.save_event(oevent)
        self.publish(oevent)
        self.after_processing()

    def process(self, ievent=None):
        res = ievent or {}
        for processor in self.processors:
            res = processor.process(**res)
        return res

    def publish(self, oevent):
        self.publisher.publish(self.river.ochannel, json.dumps(oevent))

    def before_processing(self, *args, **kwargs):
        pass

    def after_processing(self, *args, **kwargs):
        pass

    def stage_input(self, channel=None, ievent=None):
        pass

    def save_event(self, event):
        events.create_event(self.river, event)

    def processor(self, index):
        def decorator(f):
            proc = RiverProcessor(f)
            self.processors.insert(index-1, proc)
            return f
        return decorator

    def structure_output(self, timestamp, result):
        res = {}
        meta = {}
        meta['timestamp'] = timestamp
        meta['river'] = self.river.name
        res['metadata'] = meta
        res['data'] = result
        return res

class River(EventManager):

    def __init__(self):
        self.processors = []

    def init(self, schema):
        self.river = RiverService.create(schema)
        self.publisher = redis.Redis()

    def run(self):
        for channel in self.river.ichannels:
            listener = Listener(channel, self)
            listener.start()

    def stage_ievent(self, channel, ievent):
        event = json.loads(ievent['data'])
        timestamp = event['metadata']['timestamp']
        channel_events = self.aggregator.get(timestamp, {})
        # TODO: possible we overwrite an event here on a larger time interval
        channel_events[channel] = event
        self.aggregator[timestamp] = channel_events
        for channel in self.river.ichannels:
            if channel not in channel_events:
                return
        self.handle(timestamp, channel_events)

    def build_oevent(self, river, timestamp, channel_events):
        oevent = {}
        metadata = {}
        data = {}
        metadata['timestamp'] = timestamp
        metadata['river'] = river.name
        for key, path in river.ischema.iteritems():
            if key == "_comment":
                continue
            data[key] = self.get_value(path, channel_events)
        oevent['data'] = data
        oevent['metadata'] = metadata
        return oevent

    def get_value(self, path, events):
        tokens = path.split('.')
        if not tokens:
            return None
        curr = events[tokens[0]]
        for token in tokens[1:]:
            curr = curr[token]
        return curr


    def handle(self, timestamp, channel_events):
        revent = self.build_oevent(self.river, timestamp, channel_events)
        result = self.process(revent)
        oevent = self.structure_result(timestamp, result)
        self.save_event(oevent)
        self.publish(oevent)


    def process(self, event):
        res = event
        for processor in self.processors:
            res = processor.process(**event)
        return res
