from traits.api import Instance, List

from force_bdss.core.base_model import BaseModel
from force_bdss.core.kpi_specification import KPISpecification
from .parameters.base_mco_parameter import BaseMCOParameter
from .i_mco_factory import IMCOFactory


class BaseMCOModel(BaseModel):
    """Base class for the specific MCO models.
    This model will also provide, through traits/traitsui magic the View
    that will appear in the workflow manager UI.

    In your definition, your specific model must reimplement this class.
    """
    #: A reference to the creating factory, so that we can
    #: retrieve it as the originating factory.
    factory = Instance(IMCOFactory, visible=False, transient=True)

    #: A list of the parameters for the MCO
    parameters = List(BaseMCOParameter, visible=False)

    #: A list of KPI specification objects and their objective.
    kpis = List(KPISpecification, visible=False)
