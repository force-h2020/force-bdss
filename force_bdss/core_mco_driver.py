from envisage.extension_point import ExtensionPoint
from envisage.plugin import Plugin
from traits.has_traits import on_trait_change
from traits.trait_types import List

from force_bdss.data_sources.i_data_source_bundle import (
    IDataSourceBundle)
from force_bdss.kpi.i_kpi_calculator_bundle import IKPICalculatorBundle
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

    #: A list of the available Data Sources.
    #: It will be populated by plugins.
    data_source_bundles = ExtensionPoint(
        List(IDataSourceBundle),
        id='force.bdss.data_sources.bundles')

    #: A list of the available Key Performance Indicator calculators.
    #: It will be populated by plugins.
    kpi_calculator_bundles = ExtensionPoint(
        List(IKPICalculatorBundle),
        id='force.bdss.kpi_calculators.bundles')

    @on_trait_change("application:started")
    def application_started(self):
        workflow = self.application.workflow

        mco_data = workflow.multi_criteria_optimizer
        mco_bundle = self._mco_bundle_by_name(mco_data.name)
        mco_model = mco_bundle.create_model(mco_data.model_data)
        mco = mco_bundle.create_optimizer(self.application, mco_model)
        mco_communicator = mco_bundle.create_communicator(
            self.application,
            mco_model)

        if not self.application.evaluate:
            mco.run()
            return

        parameters = mco_communicator.receive_from_mco()

        ds_results = []
        for requested_ds in workflow.data_sources:
            ds_bundle = self._data_source_bundle_by_name(
                requested_ds.name)
            ds_model = ds_bundle.create_model(requested_ds.model_data)
            data_source = ds_bundle.create_data_source(
                self.application, ds_model)
            ds_results.append(data_source.run(parameters))

        kpi_results = []
        for requested_kpic in workflow.kpi_calculators:
            kpic_bundle = self._kpi_calculator_bundle_by_name(
                requested_kpic.name)
            ds_model = kpic_bundle.create_model(
                requested_kpic.model_data)
            kpi_calculator = kpic_bundle.create_data_source(
                self.application, ds_model)
            kpi_results.append(kpi_calculator.run(ds_results))

        mco_communicator.send_to_mco(kpi_results)

    def _data_source_bundle_by_name(self, name):
        for ds in self.data_source_bundles:
            if ds.name == name:
                return ds

        raise Exception("Requested data source {} but don't know "
                        "to find it.".format(name))

    def _kpi_calculator_bundle_by_name(self, name):
        for kpic in self.kpi_calculator_bundles:
            if kpic.name == name:
                return kpic

        raise Exception(
            "Requested kpi calculator {} but don't know "
            "to find it.".format(name))

    def _mco_bundle_by_name(self, name):
        for mco in self.mco_bundles:
            if mco.name == name:
                return mco

        raise Exception("Requested MCO {} but it's not available"
                        "to compute it.".format(name))
