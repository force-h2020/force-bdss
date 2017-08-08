import abc

from traits.api import ABCHasStrictTraits, Instance, String, provides
from envisage.plugin import Plugin

from .i_notification_listener_factory import INotificationListenerFactory


@provides(INotificationListenerFactory)
class BaseNotificationListenerFactory(ABCHasStrictTraits):
    id = String()

    name = String()

    plugin = Instance(Plugin)

    @abc.abstractmethod
    def create_object(self):
        """"""

    @abc.abstractmethod
    def create_model(self, model_data=None):
        """"""
