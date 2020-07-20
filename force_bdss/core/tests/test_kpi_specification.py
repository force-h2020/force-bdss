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
