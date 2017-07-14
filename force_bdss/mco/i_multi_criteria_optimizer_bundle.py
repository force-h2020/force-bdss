from traits.api import Interface, String


class IMultiCriteriaOptimizerBundle(Interface):
    name = String()

    def create_optimizer(self, application, model):
        pass

    def create_model(self, model_data):
        pass
