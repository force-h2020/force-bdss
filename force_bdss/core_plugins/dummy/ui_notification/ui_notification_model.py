from traits.api import String
from force_bdss.api import (
    BaseNotificationListenerModel, ZMQSocketURL)


class UINotificationModel(BaseNotificationListenerModel):
    #: The socket URL where the UI will be found. Synchronization port.
    sync_url = ZMQSocketURL()

    #: The socket URL where the UI will be found. PubSub port.
    pub_url = ZMQSocketURL()

    #: Unique identifier assigned by the UI to recognize the connection.
    identifier = String()
