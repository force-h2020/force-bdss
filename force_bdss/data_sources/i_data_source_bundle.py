from traits.api import Interface, String


class IDataSourceBundle(Interface):
    name = String()

    def create_data_source(self, application, model):
        pass

    def create_model(self, model_data=None):
        pass
