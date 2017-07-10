from envisage.extension_point import ExtensionPoint
from traits.api import List
from envisage.plugin import Plugin
from traits.api import on_trait_change

from force_bdss.i_key_performance_calculator import IKeyPerformanceCalculator
from force_bdss.i_multi_criteria_optimizers import IMultiCriteriaOptimizer


class WorkflowPlugin(Plugin):

    id = "force_bdss.workflow_plugin"

    key_performance_calculators = ExtensionPoint(
        List(IKeyPerformanceCalculator),
        id='force_bdss.key_performance_calculators')

    multi_criteria_optimizers = ExtensionPoint(
        List(IMultiCriteriaOptimizer),
        id='force_bdss.multi_criteria_optimizers')

    @on_trait_change("application:started")
    def application_started(self):
        for mco in self.multi_criteria_optimizers:
            mco.run()
        for kpc in self.key_performance_calculators:
            kpc.run()
