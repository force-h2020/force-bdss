from traits.api import Interface, String


class IDataSourceBundle(Interface):
    id = String()

    def create_data_source(self, application, model):
        pass

    def create_model(self, model_data=None):
        pass
