import abc
import six


class BaseDataSource(six.with_metaclass(abc.ABCMeta)):
    def __init__(self, bundle, application, model):
        self.bundle = bundle
        self.application = application
        self.model = model

    @property
    def name(self):
        return self.bundle.name

    def run(self):
        pass