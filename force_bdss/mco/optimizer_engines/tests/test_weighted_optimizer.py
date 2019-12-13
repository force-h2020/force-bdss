from unittest import TestCase

from force_bdss.tests.dummy_classes.optimizer_engine import (
    DummyOptimizerEngine,
)
from force_bdss.mco.optimizer_engines.weighted_optimizer_engine import (
    sen_scaling_method,
)


class TestSenScaling(TestCase):
    def setUp(self):
        self.optimizer = DummyOptimizerEngine()
        self.scaling_values = self.optimizer.scaling_values.tolist()

    def test_sen_scaling(self):
        scaling = sen_scaling_method(
            self.optimizer.dimension, self.optimizer._weighted_optimize
        )
        self.assertListEqual(scaling.tolist(), self.scaling_values)
