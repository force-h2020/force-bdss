import abc
import six


class BaseMCOCommunicator(six.with_metaclass(abc.ABCMeta)):
    def __init__(self, bundle, application, model):
        self.bundle = bundle
        self.application = application
        self.model = model

    @abc.abstractmethod
    def receive_from_mco(self):
        pass

    @abc.abstractmethod
    def send_to_mco(self):
        pass
