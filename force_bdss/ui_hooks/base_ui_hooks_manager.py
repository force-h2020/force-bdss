#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import HasStrictTraits, Instance

from .i_ui_hooks_factory import IUIHooksFactory


class BaseUIHooksManager(HasStrictTraits):
    #: A reference to the factory
    factory = Instance(IUIHooksFactory)

    def __init__(self, factory, *args, **kwargs):
        """Initializes the UI Hooks manager.

        Parameters
        ----------
        factory: BaseUIHooksFactory
            The factory this UI Hooks manager belongs to
        """
        self.factory = factory
        super(BaseUIHooksManager, self).__init__(*args, **kwargs)

    def before_execution(self, task):
        """Hook that is called before execution of a given evaluation.
        Gives a chance to perform operations before the temporary file is
        created with its contents and the calculation invoked.

        Parameters
        ----------
        task:
            The pyface envisage task.
        """

    def after_execution(self, task):
        """Hook that is called after execution of a given evaluation.
        Gives a chance to perform operations after the calculation finished.

        Parameters
        ----------
        task:
            The pyface envisage task.
        """

    def before_save(self, task):
        """Hook that is called just before saving a given model to disk
        in response to a user action. This does not apply to saving of
        temporary files before execution.

        Parameters
        ----------
        task:
            The pyface envisage task
        """
