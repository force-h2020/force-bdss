from envisage.api import Plugin
from traits.api import Interface, Str, Instance, Type


class IDataSourceFactory(Interface):
    """Envisage required interface for the BaseDataSourceFactory.
    You should not need to use this directly.

    Refer to the BaseDataSourceFactory for documentation.
    """
    id = Str()

    name = Str()

    data_source_class = Type(
        "force_bdss.data_sources.base_data_source.BaseDataSource",
        allow_none=False
    )

    model_class = Type(
        "force_bdss.data_sources.base_data_source_model.BaseDataSourceModel",
        allow_none=False
    )

    plugin = Instance(Plugin, allow_none=False)

    def get_data_source_class(self):
        pass

    def get_model_class(self):
        pass

    def get_name(self):
        pass

    def get_identifier(self):
        pass
