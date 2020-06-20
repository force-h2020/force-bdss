#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase

from force_bdss.api import RangedMCOParameterFactory
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory
from force_bdss.mco.optimizer_engines.aposteriori_optimizer_engine import (
    AposterioriOptimizerEngine
)
from force_bdss.tests.probe_classes.optimizer import ProbeOptimizer
from force_bdss.tests.probe_classes.evaluator import ProbeEvaluator


class TestAposterioriEngine(TestCase):

    def setUp(self):
        self.plugin = {"id": "pid", "name": "Plugin"}
        self.factory = DummyMCOFactory(self.plugin)
        self.parameters = [
            RangedMCOParameterFactory(self.factory).create_model(
                {"lower_bound": 0.0, "upper_bound": 1.0}
            )]*4

        self.engine = AposterioriOptimizerEngine(
            single_point_evaluator=ProbeEvaluator(),
            optimizer=ProbeOptimizer(),
            parameters=self.parameters
        )

    def test_init(self):
        self.assertIsInstance(self.engine, AposterioriOptimizerEngine)
        self.assertEqual("APosteriori_Optimizer", self.engine.name)
        self.assertIsInstance(self.engine.optimizer, ProbeOptimizer)

    def test___getstate__(self):
        state = self.engine.__getstate__()
        self.assertDictEqual(
            {"name": "APosteriori_Optimizer",
                "verbose_run": False},
            state,
        )

    def test_optimize(self):
        n_points = 0
        self.engine.parameters = self.parameters
        for point, kpis in self.engine.optimize():
            n_points += 1
            self.assertEqual(len(self.parameters), len(point))
            self.assertEqual(2, len(kpis))
        self.assertEqual(n_points, 10)
