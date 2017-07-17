import abc
import six


class BaseKPICalculator(six.with_metaclass(abc.ABCMeta)):
    def __init__(self, bundle, application, model):
        self.bundle = bundle
        self.application = application
        self.model = model

    @property
    def name(self):
        return self.bundle.name

    @abc.abstractmethod
    def run(self, data_source_results):
        """Executes the KPI evaluation and returns the list of results."""
        pass
