#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Instance

from force_bdss.core.base_model import BaseModel
from force_bdss.notification_listeners.i_notification_listener_factory import \
    INotificationListenerFactory


class BaseNotificationListenerModel(BaseModel):
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
