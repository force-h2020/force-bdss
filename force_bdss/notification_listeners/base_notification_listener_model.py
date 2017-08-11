from traits.api import ABCHasStrictTraits, Instance

from force_bdss.notification_listeners.i_notification_listener_factory import \
    INotificationListenerFactory


class BaseNotificationListenerModel(ABCHasStrictTraits):
    """Base class for the specific Notification Listener models.
    This model will also provide, through traits/traitsui magic the View
    that will appear in the workflow manager UI.

    In your definition, your specific model must reimplement this class.
    """
    #: A reference to the creating factory, so that we can
    #: retrieve it as the originating factory.
    factory = Instance(INotificationListenerFactory,
                       visible=False,
                       transient=True)

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        super(BaseNotificationListenerModel, self).__init__(*args, **kwargs)
