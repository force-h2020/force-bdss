import unittest

from force_bdss.mco.parameters.base_mco_parameter_factory import (
    BaseMCOParameterFactory,
)

from unittest import mock

from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter


class DummyParameter(BaseMCOParameter):
    pass


class TestBaseMCOParameter(unittest.TestCase):
    def test_instantiation(self):
        factory = mock.Mock(spec=BaseMCOParameterFactory)
        param = DummyParameter(factory)
        self.assertEqual(param.factory, factory)

    def test_from_json(self):
        factory = mock.Mock(spec=BaseMCOParameterFactory)
        factory.id = "factory_id"

        parameter_data = {"name": "name", "type": "type"}
        parameter = DummyParameter.from_json(factory, parameter_data)
        self.assertDictEqual(
            parameter.__getstate__(),
            {"id": "factory_id", "model_data": parameter_data},
        )

        self.assertDictEqual(parameter_data, {"name": "name", "type": "type"})
