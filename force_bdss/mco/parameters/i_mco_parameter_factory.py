from traits.api import Instance, Type, Unicode
from force_bdss.core.i_factory import IFactory


class IMCOParameterFactory(IFactory):
    mco_factory = Instance('force_bdss.mco.base_mco_factory.BaseMCOFactory',
                           allow_none=False)

    description = Unicode()

    model_class = Type(
        "force_bdss.mco.parameters.base_mco_parameter.BaseMCOParameter",
        allow_none=False
    )

    def get_description(self):
        """"""

    def get_model_class(self):
        """"""

    def create_model(self, data_values=None):
        """"""
