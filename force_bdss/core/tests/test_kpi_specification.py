#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase

from force_bdss.core.kpi_specification import KPISpecification


class TestKPISpecification(TestCase):

    def setUp(self):
        self.kpi = KPISpecification(name="Test")

    def test_verify_name(self):
        self.assertEqual(0, len(self.kpi.verify()))

        self.kpi.name = ""
        errors = [error.local_error for error in self.kpi.verify()]
        self.assertEqual(1, len(errors))
        self.assertIn("KPI is not named", errors)

    def test_verify_bounds(self):
        self.kpi.use_bounds = True

        self.assertEqual(0, len(self.kpi.verify()))

        self.kpi.lower_bound = 2
        errors = [error.local_error for error in self.kpi.verify()]
        self.assertEqual(1, len(errors))
        self.assertIn(
            "Upper bound value of the KPI must be greater "
            "than the lower bound value.",
            errors
        )

    def test_verify_target(self):

        self.kpi.objective = "TARGET"
        errors = [error.local_error for error in self.kpi.verify()]
        self.assertEqual(1, len(errors))
        self.assertIn("Target value must be non-zero", errors)

        self.kpi.target_value = 0.5
        self.assertEqual(0, len(self.kpi.verify()))

        self.kpi.use_bounds = True
        self.assertEqual(0, len(self.kpi.verify()))
