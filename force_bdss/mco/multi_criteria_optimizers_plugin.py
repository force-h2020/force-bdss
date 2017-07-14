from envisage.plugin import Plugin
from traits.api import List

from .i_multi_criteria_optimizer_bundle import (
    IMultiCriteriaOptimizerBundle)
from .dakota_bundle import DakotaBundle
from .basic_bundle import BasicBundle


class MultiCriteriaOptimizersPlugin(Plugin):
    id = "force.bdss.mco.plugins.multi_criteria_optimizers_plugin"

    multi_criteria_optimizers = List(
        IMultiCriteriaOptimizerBundle,
        contributes_to='force.bdss.mco.bundles'
    )

    def _multi_criteria_optimizers_default(self):
        return [BasicBundle(), DakotaBundle()]
