import abc
from traits.has_traits import ABCHasStrictTraits


class BaseKPICalculatorModel(ABCHasStrictTraits):
    @classmethod
    @abc.abstractmethod
    def from_json(self, model_data):
        pass
