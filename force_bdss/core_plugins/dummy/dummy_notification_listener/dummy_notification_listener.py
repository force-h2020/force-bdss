from force_bdss.api import BaseNotificationListener
from force_bdss.mco.events import (
    MCOStartEvent, MCOFinishEvent, MCOProgressEvent)


class DummyNotificationListener(BaseNotificationListener):
    def deliver(self, model, event):
        if isinstance(event, (MCOStartEvent, MCOFinishEvent)):
            print(event.__class__.__name__)
        elif isinstance(event, MCOProgressEvent):
            print(event.__class__.__name__, event.input, event.output)

    def init_persistent_state(self, model):
        print("Initializing persistent state")
