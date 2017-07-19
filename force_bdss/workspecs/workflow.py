from traits.api import HasStrictTraits, Instance, String, List

from ..data_sources.base_data_source_model import BaseDataSourceModel
from ..kpi.base_kpi_calculator_model import BaseKPICalculatorModel
from ..mco.base_mco_model import BaseMCOModel


class Workflow(HasStrictTraits):
    name = String()
    multi_criteria_optimizer = Instance(BaseMCOModel)
    data_sources = List(BaseDataSourceModel)
    kpi_calculators = List(BaseKPICalculatorModel)
