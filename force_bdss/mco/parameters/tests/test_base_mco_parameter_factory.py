import unittest

from force_bdss.mco.base_mco_bundle import BaseMCOBundle

try:
    import mock
except ImportError:
    from unittest import mock
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
        factory = DummyMCOParameterFactory(mock.Mock(spec=BaseMCOBundle))
        model = factory.create_model({"x": 42})
        self.assertIsInstance(model, DummyMCOParameter)
        self.assertEqual(model.x, 42)
