from traits.api import ABCHasStrictTraits, Instance, List

from .parameters.base_mco_parameter import BaseMCOParameter
from .i_mco_factory import IMCOFactory


class BaseMCOModel(ABCHasStrictTraits):
    """Base class for the specific MCO models.
    This model will also provide, through traits/traitsui magic the View
    that will appear in the workflow manager UI.

    In your definition, your specific model must reimplement this class.
    """
    #: A reference to the creating bundle, so that we can
    #: retrieve it as the originating factory.
    factory = Instance(IMCOFactory,
                       visible=False,
                       transient=True)

    # A list of the parameters for the MCO
    parameters = List(BaseMCOParameter)

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        super(BaseMCOModel, self).__init__(*args, **kwargs)
