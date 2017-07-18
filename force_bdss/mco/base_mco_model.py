import abc
import six


class BaseMCOModel(six.with_metaclass(abc.ABCMeta)):
    @abc.abstractclassmethod
    def from_json(self, model_data):
        pass
