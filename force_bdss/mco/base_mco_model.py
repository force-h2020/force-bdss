import abc
from traits.api import ABCHasStrictTraits


class BaseMCOModel(ABCHasStrictTraits):
    @classmethod
    @abc.abstractmethod
    def from_json(self, model_data):
        pass
