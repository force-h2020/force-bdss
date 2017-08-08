from force_bdss.api import BaseNotificationListener


class DummyNotificationListener(BaseNotificationListener):
    def deliver(self, model, message):
        print(message)
