from traits.api import String

from force_bdss.api import factory_id, BaseDataSourceFactory

from .power_evaluator_model import PowerEvaluatorModel
from .power_evaluator_data_source import PowerEvaluatorDataSource


class PowerEvaluatorFactory(BaseDataSourceFactory):
    id = String(factory_id("enthought", "power_evaluator"))

    name = String("Power Evaluator")

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}

        return PowerEvaluatorModel(self, **model_data)

    def create_data_source(self):
        return PowerEvaluatorDataSource(self)
