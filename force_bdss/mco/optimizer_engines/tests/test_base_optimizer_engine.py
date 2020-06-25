#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase

from force_bdss.api import KPISpecification, RangedMCOParameterFactory
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory
from force_bdss.tests.dummy_classes.optimizer_engine import (
    DummyOptimizerEngine,
)
from force_bdss.tests.probe_classes.workflow_file import ProbeWorkflowFile
from force_bdss.tests import fixtures


class TestBaseOptimizerEngine(TestCase):
    def setUp(self):
        self.plugin = {"id": "pid", "name": "Plugin"}
        self.factory = DummyMCOFactory(self.plugin)
        workflow_file = ProbeWorkflowFile(path=fixtures.get("test_probe.json"))
        workflow_file.read()
        self.workflow = workflow_file.workflow

        self.parameters = [1, 1, 1, 1]
        self.optimizer_engine = DummyOptimizerEngine(
            single_point_evaluator=self.workflow
        )

    def test_initialize(self):
        self.assertListEqual([], self.optimizer_engine.parameters)
        self.assertListEqual([], self.optimizer_engine.kpis)

    def test_base_methods(self):
        point = [1.0]
        kpi_values = self.workflow.evaluate(point)
        score = self.optimizer_engine._score(point)

        self.assertDictEqual(
            {(1.0,): kpi_values}, self.optimizer_engine._kpi_cache
        )
        self.assertEqual(0, score.size)

    def test_parameter_bounds(self):
        self.optimizer_engine.parameters = [
            RangedMCOParameterFactory(self.factory).create_model(
                {"lower_bound": 0.0, "upper_bound": 1.0}
            )
            for _ in self.parameters
        ]

        self.assertListEqual(
            self.optimizer_engine.initial_parameter_value,
            [0.5] * len(self.parameters),
        )
        self.assertListEqual(
            self.optimizer_engine.parameter_bounds,
            [(0.0, 1.0)] * len(self.parameters),
        )

    def test_kpi_bounds(self):
        self.optimizer_engine.kpis = [
            KPISpecification(
                lower_bound=0.0, upper_bound=1.0
            )
        ]

        self.assertListEqual(
            [(0.0, 1.0)],
            self.optimizer_engine.kpi_bounds,
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

    def test_get_kpi_cache_key(self):

        input_point = ['a', 1, 'list']
        self.assertEqual(
            ('a', 1, 'list'),
            self.optimizer_engine._get_kpi_cache_key(input_point)
        )

        input_point = ['a', 1, ['nested'], 'list']
        self.assertEqual(
            ('a', 1, ('nested',), 'list'),
            self.optimizer_engine._get_kpi_cache_key(input_point)
        )

        input_point = ['a', 1, (['complex'], 'structured'), 'list']
        self.assertEqual(
            ('a', 1, (('complex',), 'structured'), 'list'),
            self.optimizer_engine._get_kpi_cache_key(input_point)
        )

    def test_cache_result(self):
        input_point = ['a', 1, 'list']
        kpi_values = [4, 8, 1.0]

        self.optimizer_engine.cache_result(
            input_point, kpi_values
        )
        self.assertDictEqual(
            {('a', 1, 'list'): [4, 8, 1.0]},
            self.optimizer_engine._kpi_cache
        )

    def test_retrieve_result(self):
        self.optimizer_engine._kpi_cache = {
            ('a', 1, 'list'): [4, 8, 1.0]
        }

        input_point = ['a', 1, 'list']
        kpi_values = self.optimizer_engine.retrieve_result(
            input_point)
        self.assertEqual([4, 8, 1.0], kpi_values)

    def test___getstate__(self):
        state_dict = self.optimizer_engine.__getstate__()
        self.assertEqual(1, len(state_dict))
        self.assertEqual(False, state_dict["verbose_run"])
