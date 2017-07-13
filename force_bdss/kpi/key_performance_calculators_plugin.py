from envisage.plugin import Plugin
from traits.api import List

from force_bdss.kpi.i_key_performance_calculator import (
    IKeyPerformanceCalculator)

from force_bdss.kpi.basic import Basic
from force_bdss.kpi.price import Price
from force_bdss.kpi.viscosity import Viscosity


class KeyPerformanceCalculatorsPlugin(Plugin):

    id = "force_bdss.key_performance_calculators_plugin"

    key_performance_calculators = List(
        IKeyPerformanceCalculator,
        contributes_to='force_bdss.key_performance_calculators'
    )

    def _key_performance_calculators_default(self):
        return [Basic(), Viscosity(), Price()]
