import abc
from traits.api import ABCHasStrictTraits


class BaseUIHookManager(ABCHasStrictTraits):
    @abc.abstractmethod
    def before_execution(self, application, model):
        """Hook that is called before execution of a given model.
        Gives a chance to alter the model before the temporary file is created
        with its contents and the calculation invoked.
        """

    @abc.abstractmethod
    def before_save(self, application, model):
        """Hook that is called just before saving a given model to disk
        in response to a user action. This does not apply to saving of
        temporary files before execution.
        """
