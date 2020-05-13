#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Instance, Type
from force_bdss.core.i_factory import IFactory


class IMCOParameterFactory(IFactory):

    mco_factory = Instance('force_bdss.mco.base_mco_factory.BaseMCOFactory',
                           allow_none=False)

    model_class = Type(
        "force_bdss.mco.parameters.base_mco_parameter.BaseMCOParameter",
        allow_none=False
    )

    def get_model_class(self):
        """Returns type of BaseMCOParameter subclass"""

    def create_model(self, data_values=None):
        """Returns instance of BaseMCOParameter subclass"""
