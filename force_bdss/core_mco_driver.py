from envisage.extension_point import ExtensionPoint
from envisage.plugin import Plugin
from traits.has_traits import on_trait_change
from traits.trait_types import List

from force_bdss.kpi.i_key_performance_calculator import (
    IKeyPerformanceCalculator)
from force_bdss.mco.i_multi_criteria_optimizers import IMultiCriteriaOptimizer


class CoreMCODriver(Plugin):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    # Note: we are forced to declare these extensions points here instead
    # of the application object, and this is why we have to use this plugin.
    # It is a workaround to an envisage bug that does not find the extension
    # points if declared on the application.

    #: A List of the available Multi Criteria Optimizers.
    #: This will be populated by MCO plugins.
    multi_criteria_optimizers = ExtensionPoint(
        List(IMultiCriteriaOptimizer),
        id='force_bdss.multi_criteria_optimizers')

    #: A list of the available Key Performance Indicator calculators.
    #: It will be populated by plugins.
    key_performance_calculators = ExtensionPoint(
        List(IKeyPerformanceCalculator),
        id='force_bdss.key_performance_calculators')

    @on_trait_change("application:started")
    def application_started(self):
        workflow = self.application.workflow
        if self.application.evaluate:
            for kpi in workflow.key_performance_indicators:
                kpc = self._find_kpc_by_computes(kpi)
                if kpc:
                    kpc.run(self.application)
                else:
                    raise Exception("Requested KPI {} but don't know how"
                                    "to compute it.".format(kpi))
        else:
            mco_name = workflow.multi_criteria_optimization.name
            mco = self._find_mco_by_name(mco_name)
            if mco:
                mco.run(self.application)
            else:
                raise Exception("Requested MCO {} but it's not available"
                                "to compute it.".format(mco_name))

    def _find_kpc_by_computes(self, computes):
        for kpc in self.key_performance_calculators:
            if kpc.computes == computes:
                return kpc

        return None

    def _find_mco_by_name(self, name):
        for mco in self.multi_criteria_optimizers:
            if mco.name == name:
                return mco

        return None
