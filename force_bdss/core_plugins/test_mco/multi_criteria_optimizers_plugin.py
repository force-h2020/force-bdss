from envisage.plugin import Plugin
from traits.api import List

from force_bdss.mco.i_multi_criteria_optimizer_bundle import (
    IMultiCriteriaOptimizerBundle)

from .dakota.dakota_bundle import DakotaBundle


class MultiCriteriaOptimizersPlugin(Plugin):
    multi_criteria_optimizers = List(
        IMultiCriteriaOptimizerBundle,
        contributes_to='force.bdss.mco.bundles'
    )

    def _multi_criteria_optimizers_default(self):
        return [DakotaBundle()]
