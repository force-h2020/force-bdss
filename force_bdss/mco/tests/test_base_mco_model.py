import testfixtures
import unittest
import warnings

from force_bdss.mco.base_mco import NotifyEventWarning
from force_bdss.tests.dummy_classes.factory_registry import (
    DummyFactoryRegistry,
)


class TestNotifyEventWarning(unittest.TestCase):
    """NOTE: this class should be removed alongside BaseMCO.event"""
    def test_warn(self):

        expected_message = (
            "Use of the BaseMCO.event attribute is now deprecated and will"
            " be removed in version 0.5.0. Please replace any uses of the "
            "BaseMCO.notify and BaseMCO.notify_new_point method with the "
            "equivalent BaseMCOModel.notify and "
            "BaseMCOModel.notify_new_point methods respectively")

        expected_log = (
            "force_bdss.mco.base_mco",
            "WARNING",
            expected_message,
        )

        with testfixtures.LogCapture() as capture, \
                warnings.catch_warnings(record=True) as errors:

            NotifyEventWarning.warn()

            capture.check(expected_log)
            self.assertEqual(expected_message, str(errors[0].message))


class TestBaseMCOModel(unittest.TestCase):
    def setUp(self):
        factory_registry = DummyFactoryRegistry()
        self.mcomodel_factory = factory_registry.mco_factories[0]

    def test_from_json(self):
        empty_data = {
            "parameters": [
                {
                    "id": "force.bdss.enthought.plugin."
                          "test.v0.factory.dummy_mco.parameter."
                          "dummy_mco_parameter",
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
                "id": "force.bdss.enthought.plugin.test.v0."
                      "factory.dummy_mco",
                "model_data": {
                    "parameters": [
                        {
                            "id": "force.bdss.enthought.plugin."
                                  "test.v0.factory.dummy_mco."
                                  "parameter.dummy_mco_parameter",
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
                        "id": "force.bdss.enthought.plugin."
                              "test.v0.factory.dummy_mco."
                              "parameter.dummy_mco_parameter",
                        "model_data": {},
                    }
                ],
                "kpis": [],
            },
        )
