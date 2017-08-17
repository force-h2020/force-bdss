import unittest

from force_bdss.core_plugins.dummy.tests.data_source_factory_test_mixin \
    import DataSourceFactoryTestMixin
from force_bdss.core_plugins.dummy.power_evaluator.power_evaluator_factory import PowerEvaluatorFactory  # noqa
from force_bdss.core_plugins.dummy.power_evaluator.power_evaluator_data_source import PowerEvaluatorDataSource  # noqa
from force_bdss.core_plugins.dummy.power_evaluator.power_evaluator_model import PowerEvaluatorModel  # noqa


class TestPowerEvaluatorFactory(DataSourceFactoryTestMixin,
                                unittest.TestCase):
    @property
    def factory_class(self):
        return PowerEvaluatorFactory

    @property
    def model_class(self):
        return PowerEvaluatorModel

    @property
    def data_source_class(self):
        return PowerEvaluatorDataSource
