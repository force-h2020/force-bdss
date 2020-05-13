#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
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

    def test_instantiation(self):
        mco_factory = ProbeMCOFactory(self.plugin)
        factory = ProbeParameterFactory(mco_factory)
        param = ProbeParameter(factory)
        self.assertEqual(param.factory, factory)

    def test_from_json(self):
        mco_factory = ProbeMCOFactory(self.plugin)
        parameter_factory = mco_factory.parameter_factories[0]

        parameter_data = {"name": "name", "type": "type"}
        parameter = ProbeParameter.from_json(parameter_factory, parameter_data)
        self.assertDictEqual(
            parameter.__getstate__(),
            {
                "id": "force.bdss.enthought.plugin.test.v0.factory."
                      "probe_mco.parameter.probe_mco_parameter",
                "model_data": parameter_data,
            },
        )

        self.assertDictEqual(parameter_data, {"name": "name", "type": "type"})
