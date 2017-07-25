import unittest
from traits.api import Int


from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory


class DummyMCOParameter(BaseMCOParameter):
    x = Int()


class DummyMCOParameterFactory(BaseMCOParameterFactory):
    id = "foo"
    name = "bar"
    description = "baz"
    model_class = DummyMCOParameter


class TestBaseMCOParameterFactory(unittest.TestCase):
    def test_initialization(self):
        factory = DummyMCOParameterFactory()
        model = factory.create_model({"x": 42})
        self.assertIsInstance(model, DummyMCOParameter)
        self.assertEqual(model.x, 42)
