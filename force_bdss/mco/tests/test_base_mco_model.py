import unittest

from force_bdss.tests.dummy_classes.factory_registry import (
    DummyFactoryRegistry,
)


class TestBaseMCOModel(unittest.TestCase):
    def setUp(self):
        factory_registry = DummyFactoryRegistry()
        self.mcomodel_factory = factory_registry.mco_factories[0]

    def test_from_json(self):
        empty_data = {
            "parameters": [
                {
                    "id": "force.bdss.enthought.plugin.test.v0.factory.dummy_mco.parameter.dummy_mco_parameter",
                    "model_data": {},
                }
            ],
            "kpis": [],
        }
        mco_model = self.mcomodel_factory.model_class.from_json(
            self.mcomodel_factory, empty_data
        )
        self.assertDictEqual(
            mco_model.__getstate__(),
            {
                "id": "force.bdss.enthought.plugin.test.v0.factory.dummy_mco",
                "model_data": {
                    "parameters": [
                        {
                            "id": "force.bdss.enthought.plugin.test.v0.factory.dummy_mco.parameter.dummy_mco_parameter",
                            "model_data": {"x": 0, "name": "", "type": ""},
                        }
                    ],
                    "kpis": [],
                },
            },
        )

        self.assertDictEqual(
            empty_data,
            {
                "parameters": [
                    {
                        "id": "force.bdss.enthought.plugin.test.v0.factory.dummy_mco.parameter.dummy_mco_parameter",
                        "model_data": {},
                    }
                ],
                "kpis": [],
            },
        )
