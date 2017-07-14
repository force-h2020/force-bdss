from envisage.plugin import Plugin
from traits.api import List

from force_bdss.data_sources.basic_bundle import BasicBundle
from force_bdss.data_sources.price_bundle import PriceBundle
from force_bdss.data_sources.viscosity_bundle import ViscosityBundle
from .i_data_source_bundle import IDataSourceBundle


class DataSourcesPlugin(Plugin):
    id = "force_bdss.data_sources_plugin"

    data_sources = List(
        IDataSourceBundle,
        contributes_to='force.bdss.data_sources.bundles'
    )

    def _data_sources_default(self):
        return [BasicBundle(),
                ViscosityBundle(),
                PriceBundle()]
