from traits.api import String

from force_bdss.api import factory_id, BaseNotificationListenerFactory

from .ui_notification import UINotification
from .ui_notification_model import UINotificationModel


class UINotificationFactory(BaseNotificationListenerFactory):
    id = String(factory_id("enthought", "ui_notification"))

    name = String("UI Notification")

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}

        return UINotificationModel(self, **model_data)

    def create_listener(self):
        return UINotification(self)
