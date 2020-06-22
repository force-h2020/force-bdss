#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase

from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.mco.optimizer_engines.utilities import (
    convert_to_score)


class TestConvertUtil(TestCase):
    def test_convert_to_score(self):
        kpis = [
            KPISpecification(objective="MINIMISE"),
            KPISpecification(objective="MAXIMISE"),
            KPISpecification(objective="TARGET", target_value=10)
        ]
        values = [10.0, 20.0, 15.0]
        inv_values = convert_to_score(values, kpis)
        self.assertListEqual(list(inv_values), [10.0, -20.0, 5.0])
