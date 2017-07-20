from traits.api import HasStrictTraits, Instance, List

from ..data_sources.base_data_source_model import BaseDataSourceModel
from ..kpi.base_kpi_calculator_model import BaseKPICalculatorModel
from ..mco.base_mco_model import BaseMCOModel


class Workflow(HasStrictTraits):
    multi_criteria_optimizer = Instance(BaseMCOModel, allow_none=True)
    data_sources = List(BaseDataSourceModel)
    kpi_calculators = List(BaseKPICalculatorModel)
