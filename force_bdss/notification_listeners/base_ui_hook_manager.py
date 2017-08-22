import abc
from traits.api import ABCHasStrictTraits


class BaseUIHookManager(ABCHasStrictTraits):
    @abc.abstractmethod
    def before_execution(self, application, model):
        """Hook that is called before execution of a given model.
        Gives a chance to alter the model before the temporary file is created
        with its contents and the calculation invoked.
        """
