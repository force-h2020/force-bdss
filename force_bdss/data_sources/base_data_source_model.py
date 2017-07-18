import abc
import six


class BaseDataSourceModel(six.with_metaclass(abc.ABCMeta)):
    @abc.abstractclassmethod
    def from_json(self, model_data):
        pass
