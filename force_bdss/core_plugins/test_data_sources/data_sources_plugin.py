from envisage.plugin import Plugin
from traits.api import List

from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle

from .basic.basic_bundle import BasicBundle
from .price.price_bundle import PriceBundle
from .viscosity.viscosity_bundle import ViscosityBundle


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
