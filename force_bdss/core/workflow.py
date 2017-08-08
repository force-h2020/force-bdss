from traits.api import HasStrictTraits, Instance, List

from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.kpi.base_kpi_calculator_model import BaseKPICalculatorModel
from force_bdss.mco.base_mco_model import BaseMCOModel


class Workflow(HasStrictTraits):
    """Model object that represents the Workflow as a whole"""
    #: Contains the factory-specific MCO Model object.
    #: Can be None if no MCO has been specified yet.
    mco = Instance(BaseMCOModel, allow_none=True)

    #: Contains the factory-specific DataSource Model objects.
    #: The list can be empty
    data_sources = List(BaseDataSourceModel)

    #: Contains the factory-specific KPI Calculator Model objects.
    #: The list can be empty
    kpi_calculators = List(BaseKPICalculatorModel)
