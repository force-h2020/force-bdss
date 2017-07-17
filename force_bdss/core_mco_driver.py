from envisage.extension_point import ExtensionPoint
from envisage.plugin import Plugin
from traits.has_traits import on_trait_change
from traits.trait_types import List

from force_bdss.data_sources.i_data_source_bundle import (
    IDataSourceBundle)
from force_bdss.mco.i_multi_criteria_optimizer_bundle import (
    IMultiCriteriaOptimizerBundle)


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
    mco_bundles = ExtensionPoint(
        List(IMultiCriteriaOptimizerBundle),
        id='force.bdss.mco.bundles')

    #: A list of the available Key Performance Indicator calculators.
    #: It will be populated by plugins.
    data_source_bundles = ExtensionPoint(
        List(IDataSourceBundle),
        id='force.bdss.data_sources.bundles')

    @on_trait_change("application:started")
    def application_started(self):
        workflow = self.application.workflow
        if self.application.evaluate:
            ds_results = []
            for requested_ds in workflow.data_sources:
                ds_bundle = self._find_data_source_bundle_by_name(
                    requested_ds.name)
                if ds_bundle:
                    ds_model = ds_bundle.create_model(requested_ds.model_data)
                    data_source = ds_bundle.create_data_source(
                        self.application, ds_model)
                    ds_results.append(data_source.run())
                else:
                    raise Exception("Requested data source {} but don't know "
                                    "to find it.".format(requested_ds.name))
        else:
            mco_data = workflow.multi_criteria_optimizer
            mco_bundle = self._find_mco_bundle_by_name(mco_data.name)
            if mco_bundle:
                mco_model = mco_bundle.create_model(mco_data.model_data)
                mco = mco_bundle.create_optimizer(self.application, mco_model)
                mco.run()
            else:
                raise Exception("Requested MCO {} but it's not available"
                                "to compute it.".format(mco_data.name))

    def _find_data_source_bundle_by_name(self, name):
        for ds in self.data_source_bundles:
            if ds.name == name:
                return ds

        return None

    def _find_mco_bundle_by_name(self, name):
        for mco in self.mco_bundles:
            if mco.name == name:
                return mco

        return None
