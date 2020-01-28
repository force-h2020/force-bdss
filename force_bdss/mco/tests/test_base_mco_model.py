import unittest
import testfixtures
import warnings

from traits.testing.api import UnittestTools

from force_bdss.mco.base_mco_model import NotifyMCOProgressWarning
from force_bdss.core.data_value import DataValue
from force_bdss.tests.dummy_classes.factory_registry import (
    DummyFactoryRegistry,
)
from force_bdss.tests.probe_classes.workflow_file import ProbeWorkflowFile
from force_bdss.tests import fixtures


class TestBaseMCOModel(unittest.TestCase, UnittestTools):
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

    def test_notify_events(self):
        workflow_file = ProbeWorkflowFile(path=fixtures.get("test_probe.json"))
        workflow_file.read()
        workflow = workflow_file.workflow

        with self.assertTraitChanges(workflow, "event", count=1):
            with self.assertTraitChanges(workflow.mco_model, "event", count=1):
                workflow.mco_model.notify_start_event()

        with self.assertTraitChanges(workflow, "event", count=1):
            with self.assertTraitChanges(workflow.mco_model, "event", count=1):
                workflow.mco_model.notify_finish_event()

        with self.assertTraitChanges(workflow, "event", count=1):
            with self.assertTraitChanges(workflow.mco_model, "event", count=1):
                workflow.mco_model.notify_progress_event(
                    [DataValue(value=2), DataValue(value=3)],
                    [DataValue(value=4), DataValue(value=5)]
                )

        # NOTE: this functionality is deprecated and therefore the test
        # should be removed alongside BaseMCOModel.notify_new_point
        with self.assertTraitChanges(workflow, "event", count=1):
            with self.assertTraitChanges(workflow.mco_model, "event", count=1):
                workflow.mco_model.notify_new_point(
                    [DataValue(value=2), DataValue(value=3)],
                    [DataValue(value=4), DataValue(value=5)],
                    weights=[1.5, 1.5],
                )


class TestNotifyMCOProgressWarning(unittest.TestCase):
    """NOTE: this class should be removed alongside BaseMCO.event"""

    def test_warn(self):

        expected_message = (
            "Use of the BaseMCOModel.notify_new_point method is now deprecated"
            " and will be removed in version 0.5.0. Please replace any uses "
            "of the BaseMCO.notify_new_point method with the "
            "equivalent BaseMCOModel.notify_progress_event method."
        )

        expected_log = (
            "force_bdss.mco.base_mco_model",
            "WARNING",
            expected_message,
        )

        with testfixtures.LogCapture() as capture, warnings.catch_warnings(
            record=True
        ) as errors:

            NotifyMCOProgressWarning.warn()

            capture.check(expected_log)
            self.assertEqual(expected_message, str(errors[0].message))
