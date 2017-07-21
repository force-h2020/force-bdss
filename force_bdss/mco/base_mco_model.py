from traits.api import ABCHasStrictTraits, Instance, List

from ..workspecs.mco_parameters import MCOParameter
from .i_multi_criteria_optimizer_bundle import IMultiCriteriaOptimizerBundle


class BaseMCOModel(ABCHasStrictTraits):
    """Base class for the bundle specific MCO models.
    This model will also provide, through traits/traitsui magic the View
    that will appear in the workflow manager UI.

    In your bundle definition, your bundle-specific model must reimplement
    this class.
    """
    #: A reference to the creating bundle, so that we can
    #: retrieve it as the originating factory.
    bundle = Instance(IMultiCriteriaOptimizerBundle,
                      visible=False,
                      transient=True)

    parameters = List(MCOParameter)

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseMCOModel, self).__init__(*args, **kwargs)
