import abc
import six


class BaseDataSourceModel(six.with_metaclass(abc.ABCMeta)):
    @classmethod
    @abc.abstractmethod
    def from_json(self, model_data):
        pass
