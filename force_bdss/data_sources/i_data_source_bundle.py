from traits.api import Interface, String


class IDataSourceBundle(Interface):
    #: Unique identifier that identifies the bundle uniquely in the
    #: universe of bundles. Create one with the function bundle_id()
    id = String()

    #: A human readable name of the bundle
    name = String()

    def create_data_source(self):
        """Factory method.
        Must return the bundle-specific BaseDataSource instance.
        """

    def create_model(self, model_data=None):
        """Factory method.
        Must return the bundle-specific BaseDataSourceModel instance.
        """
