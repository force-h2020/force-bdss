from traits.api import Type, List

from force_bdss.core.i_factory import IFactory


class IMCOFactory(IFactory):
    """Interface for the BaseMCOFactory.
    You should not need it, as its main use is for envisage support.

    Refer to BaseMCOFactory for documentation
    """
    optimizer_class = Type(
        "force_bdss.mco.base_mco.BaseMCO",
        allow_none=False
    )

    model_class = Type(
        "force_bdss.mco.base_mco_communicator.BaseMCOCommunicator",
        allow_none=False

    )

    communicator_class = Type(
        "force_bdss.mco.base_mco_model.BaseMCOModel",
        allow_none=False
    )

    parameter_factory_classes = List(Type(
        "force_bdss.mco.parameters.i_mco_parameter_factory"
        ".IMCOParameterFactory"))

    def get_model_class(self):
        """
        :return: model class.
        """

    def get_communicator_class(self):
        """
        :return: model communicator class.
        """

    def get_optimizer_class(self):
        """
        :return: optimizer class
        """

    def get_parameter_factory_classes(self):
        """Returns a list of classes that provide the
        IMCOParameterFactory interface"""

    def create_optimizer(self):
        """
        :return: optimizer
        """

    def create_model(self):
        """
        :return: model
        """

    def create_communicator(self):
        """
        :return: communicator
        """
