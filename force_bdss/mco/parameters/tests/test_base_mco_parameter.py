import unittest

from traits.api import Float, Any

from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.core.ontology import BDSSOntology
from force_bdss.tests.probe_classes.mco import (
    ProbeParameterFactory,
    ProbeParameter,
)
from force_bdss.tests.probe_classes.factory_registry import (
    ProbeFactoryRegistry,
    ProbeMCOFactory,
)


class DummyParameter(BaseMCOParameter):
    pass


class TestBaseMCOParameter(unittest.TestCase):
    def setUp(self):
        self.registry = ProbeFactoryRegistry()
        self.plugin = self.registry.plugin
        self.mco_factory = ProbeMCOFactory(self.plugin)

    def test_instantiation(self):
        factory = ProbeParameterFactory(self.mco_factory)
        param = ProbeParameter(factory)
        self.assertEqual(param.factory, factory)

    def test_trait_type(self):
        parameter_factory = self.mco_factory.parameter_factories[0]
        parameter = parameter_factory.create_model()

        self.assertEqual('Value', parameter.type)

        ontology = BDSSOntology()
        self.assertEqual(
            Any, parameter.trait_type(ontology))

        parameter.type = 'Volume'
        self.assertEqual(
            Float, parameter.trait_type(ontology))

    def test_from_json(self):
        parameter_factory = self.mco_factory.parameter_factories[0]

        parameter_data = {"name": "name", "type": "Type"}
        parameter = ProbeParameter.from_json(parameter_factory, parameter_data)
        self.assertDictEqual(
            {
                "id": "force.bdss.enthought.plugin.test.v0.factory."
                      "probe_mco.parameter.probe_mco_parameter",
                "model_data": parameter_data,
            },
            parameter.__getstate__()
        )

        self.assertDictEqual(
            {"name": "name", "type": "Type"},
            parameter_data
        )
