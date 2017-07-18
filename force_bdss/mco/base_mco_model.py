import abc
import six


class BaseMCOModel(six.with_metaclass(abc.ABCMeta)):
    @classmethod
    @abc.abstractmethod
    def from_json(self, model_data):
        pass
