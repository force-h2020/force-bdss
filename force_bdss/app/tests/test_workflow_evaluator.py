from unittest import TestCase

from force_bdss.tests import fixtures
from force_bdss.tests.probe_classes.workflow_file import ProbeWorkflowFile

from force_bdss.core.workflow import Workflow
from force_bdss.app.workflow_evaluator import WorkflowEvaluator


class TestWorkflowEvaluator(TestCase):
    def setUp(self):
        file_path = "test_probe.json"
        workflow_file = ProbeWorkflowFile(path=fixtures.get("test_probe.json"))
        workflow_file.read()
        self.evaluator = WorkflowEvaluator(
            workflow=workflow_file.workflow
        )

    def test_empty_init(self):

        evaluator = WorkflowEvaluator()
        self.assertIsNone(evaluator.workflow)

    def test_init(self):

        self.assertIsInstance(self.evaluator.workflow, Workflow)
        self.assertEqual(
            self.evaluator.workflow.mco_model, self.evaluator.mco_model
        )

    def test__internal_evaluate(self):

        kpi_results = self.evaluator._internal_evaluate([1.0])
        self.assertEqual(1, len(kpi_results))

    def test_evaluate(self):

        kpi_results = self.evaluator.evaluate([1.0])

        self.assertEqual(1, len(kpi_results))
        self.assertIsNone(kpi_results[0])
