import abc
from traits.api import ABCHasStrictTraits, Instance

from .i_ui_hooks_factory import IUIHooksFactory


class BaseUIHookManager(ABCHasStrictTraits):
    #: A reference to the factory
    factory = Instance(IUIHooksFactory)

    def __init__(self, factory, *args, **kwargs):
        """Initializes the notification listener.

        Parameters
        ----------
        factory: BaseNotificationListener
            The factory this Notification Listener belongs to
        """
        self.factory = factory
        super(BaseUIHookManager, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def before_execution(self, task):
        """Hook that is called before execution of a given evaluation.
        Gives a chance to perform operations before the temporary file is
        created with its contents and the calculation invoked.

        Parameters
        ----------
        task:
            The pyface envisage task.
        """

    @abc.abstractmethod
    def before_save(self, task):
        """Hook that is called just before saving a given model to disk
        in response to a user action. This does not apply to saving of
        temporary files before execution.

        Parameters
        ----------
        task:
            The pyface envisage task
        """
