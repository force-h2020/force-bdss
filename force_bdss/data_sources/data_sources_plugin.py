from envisage.plugin import Plugin
from traits.api import List

from force_bdss.data_sources.i_data_source import (
    IDataSource)

from force_bdss.data_sources.basic import Basic
from force_bdss.data_sources.price import Price
from force_bdss.data_sources.viscosity import Viscosity


class DataSourcesPlugin(Plugin):

    id = "force_bdss.data_sources_plugin"

    data_sources = List(
        IDataSource,
        contributes_to='force_bdss.data_sources'
    )

    def _data_sources_default(self):
        return [Basic(), Viscosity(), Price()]
