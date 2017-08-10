from force_bdss.api import (
    BaseNotificationListener,
    MCOStartEvent,
    MCOFinishEvent,
    MCOProgressEvent
)


class DummyNotificationListener(BaseNotificationListener):
    def deliver(self, event):
        if isinstance(event, (MCOStartEvent, MCOFinishEvent)):
            print(event.__class__.__name__)
        elif isinstance(event, MCOProgressEvent):
            print(event.__class__.__name__, event.input, event.output)
        else:
            print(event.__class__.__name__)

    def initialize(self, model):
        print("Initializing")

    def finalize(self):
        print("Finalizing")
