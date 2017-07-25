from traits.api import HasStrictTraits, String, Instance

from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory


class BaseMCOParameter(HasStrictTraits):
    """The base class of all MCO Parameter models.
    Must be reimplemented by specific classes handling the specific parameter
    that MCOs understand.
    """
    factory = Instance(BaseMCOParameterFactory)
    value_name = String()
    value_type = String()

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        super(BaseMCOParameter, self).__init__(*args, **kwargs)
