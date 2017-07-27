from traits.api import ABCHasStrictTraits, Instance, List

from .parameters.base_mco_parameter import BaseMCOParameter
from .i_mco_bundle import IMCOBundle


class BaseMCOModel(ABCHasStrictTraits):
    """Base class for the bundle specific MCO models.
    This model will also provide, through traits/traitsui magic the View
    that will appear in the workflow manager UI.

    In your bundle definition, your bundle-specific model must reimplement
    this class.
    """
    #: A reference to the creating bundle, so that we can
    #: retrieve it as the originating factory.
    bundle = Instance(IMCOBundle,
                      visible=False,
                      transient=True)

    # A list of the parameters for the MCO
    parameters = List(BaseMCOParameter)

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseMCOModel, self).__init__(*args, **kwargs)
