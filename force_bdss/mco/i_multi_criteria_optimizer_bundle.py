from traits.api import Interface, String


class IMultiCriteriaOptimizerBundle(Interface):
    id = String()

    name = String()

    def create_optimizer(self, application, model):
        pass

    def create_model(self, model_data=None):
        pass

    def create_communicator(self, model_data):
        pass
