from traits.api import HasStrictTraits, Instance, List

from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.kpi.base_kpi_calculator_model import BaseKPICalculatorModel
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.notification_listeners.base_notification_listener_model \
    import BaseNotificationListenerModel


class Workflow(HasStrictTraits):
    """Model object that represents the Workflow as a whole"""
    #: Contains the factory-specific MCO Model object.
    #: Can be None if no MCO has been specified yet.
    mco = Instance(BaseMCOModel, allow_none=True)

    #: The execution layers. Execution starts from the first layer,
    #: where all data sources are executed in sequence. It then passes all
    #: the computed data to the second layer, then the third etc.
    #: For now, the final execution is performed by the KPI layer, but this
    #: will go away when we remove the KPI calculators.
    execution_layers = List(List(BaseDataSourceModel))

    #: Contains the factory-specific KPI Calculator Model objects.
    #: The list can be empty
    kpi_calculators = List(BaseKPICalculatorModel)

    #: Contains information about the listeners to be setup
    notification_listeners = List(BaseNotificationListenerModel)
