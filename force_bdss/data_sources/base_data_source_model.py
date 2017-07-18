import abc
from traits.api import ABCHasStrictTraits


class BaseDataSourceModel(ABCHasStrictTraits):
    @classmethod
    @abc.abstractmethod
    def from_json(self, model_data):
        pass
