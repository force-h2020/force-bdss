import abc
from traits.api import ABCHasStrictTraits, provides, String

from .i_data_source_bundle import IDataSourceBundle


@provides(IDataSourceBundle)
class BaseDataSourceBundle(ABCHasStrictTraits):
    #: Unique identifier that identifies the bundle uniquely in the
    #: universe of bundles. Create one with the function bundle_id()
    id = String()

    #: A human readable name of the bundle
    name = String()

    @abc.abstractmethod
    def create_data_source(self, application, model):
        """Factory method.
        Must return the bundle-specific BaseDataSource instance.
        """
        pass

    @abc.abstractmethod
    def create_model(self, model_data=None):
        """Factory method.
        Must return the bundle-specific BaseDataSourceModel instance.
        """
