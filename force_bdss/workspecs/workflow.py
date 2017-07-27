from traits.api import HasStrictTraits, Instance, List

from ..data_sources.base_data_source_model import BaseDataSourceModel
from ..kpi.base_kpi_calculator_model import BaseKPICalculatorModel
from ..mco.base_mco_model import BaseMCOModel


class Workflow(HasStrictTraits):
    """Model object that represents the Workflow as a whole"""
    #: Contains the bundle-specific MCO Model object.
    #: Can be None if no MCO has been specified yet.
    mco = Instance(BaseMCOModel, allow_none=True)

    #: Contains the bundle-specific DataSource Model objects.
    #: The list can be empty
    data_sources = List(BaseDataSourceModel)

    #: Contains the bundle-specific KPI Calculator Model objects.
    #: The list can be empty
    kpi_calculators = List(BaseKPICalculatorModel)
