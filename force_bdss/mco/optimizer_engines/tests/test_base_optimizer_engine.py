from unittest import TestCase

from force_bdss.api import KPISpecification
from force_bdss.app.workflow_evaluator import WorkflowEvaluator
from force_bdss.mco.optimizer_engines.base_optimizer_engine import (
    convert_by_mask,
)
from force_bdss.tests.dummy_classes.optimizer_engine import (
    DummyOptimizerEngine,
)
from force_bdss.tests.probe_classes.workflow_file import ProbeWorkflowFile
from force_bdss.tests import fixtures


class TestBaseOptimizerEngine(TestCase):
    def setUp(self):
        file_path = "test_probe.json"
        workflow_file = ProbeWorkflowFile(path=fixtures.get("test_probe.json"))
        workflow_file.read()
        self.evaluator = WorkflowEvaluator(
            workflow=workflow_file.workflow, workflow_filepath=file_path
        )
        self.optimizer_engine = DummyOptimizerEngine(
            single_point_evaluator=self.evaluator
        )

    def test_initialize(self):
        self.assertIs(
            self.evaluator, self.optimizer_engine.single_point_evaluator
        )
        self.assertListEqual([], self.optimizer_engine.parameters)
        self.assertListEqual([], self.optimizer_engine.kpis)

    def test_base_methods(self):
        self.assertListEqual([0.0], self.optimizer_engine.optimize())

        point = [1.0]
        self.assertListEqual(
            self.evaluator.evaluate(point), self.optimizer_engine._score(point)
        )

    def test__minimization_score(self):
        temp_kpis = [
            KPISpecification(),
            KPISpecification(objective="MAXIMISE"),
        ]
        self.optimizer_engine.kpis = temp_kpis
        score = [10.0, 20.0]
        inv_values = self.optimizer_engine._minimization_score(score)
        self.assertListEqual(list(inv_values), [10.0, -20.0])

    def test___getstate__(self):
        self.assertDictEqual(
            self.optimizer_engine.__getstate__(), {"verbose_run": False}
        )


class TestUtils(TestCase):
    def test_convert_by_mask(self):
        kpi_specs = ["MINIMISE", "MAXIMISE"]
        values = [10.0, 20.0]
        inv_values = convert_by_mask(values, kpi_specs)
        self.assertListEqual(list(inv_values), [10.0, -20.0])

        inv_values = convert_by_mask(values, kpi_specs, "MINIMISE")
        self.assertListEqual(list(inv_values), [10.0, -20.0])

        inv_values = convert_by_mask(values, kpi_specs, "MAXIMISE")
        self.assertListEqual(list(inv_values), [-10.0, 20.0])

        inv_values = convert_by_mask(values, kpi_specs, "SOMETHING")
        self.assertListEqual(list(inv_values), [-10.0, -20.0])