from copy import deepcopy
import logging

from traits.api import Instance, List

from force_bdss.core.base_model import BaseModel
from force_bdss.core_driver_events import MCOStartEvent, MCOFinishEvent
from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.core.verifier import VerifierError
from .parameters.base_mco_parameter import BaseMCOParameter
from .i_mco_factory import IMCOFactory


log = logging.getLogger(__name__)


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

    def bind_parameters(self, data_values):
        """ Bind and filter values from the MCO to the model parameters.

        Takes data values from the MCO, and binds them to the specified
        parameter names from the model.  Parameters with no name are removed.

        Parameters
        ----------
        data_values: list of DataValues
            A list of data values (usually from the MCO).

        Returns
        -------
        data_values : list of DataValues
            The data values from the MCO, ignoring those with no name.
        """
        if len(data_values) != len(self.parameters):
            error_txt = (
                "The number of data values returned by"
                " the MCO ({} values) does not match the"
                " number of parameters specified ({} values)."
                " This is either a MCO plugin error or the workflow"
                " file is corrupted."
            ).format(len(data_values), len(self.parameters))
            log.error(error_txt)
            raise RuntimeError(error_txt)

        # The data values obtained by the communicator are unnamed.
        # Assign the name to each datavalue as specified by the user.
        for dv, param in zip(data_values, self.parameters):
            dv.name = param.name

        # Exclude those who have no name set.
        return [dv for dv in data_values if dv.name != ""]

    def bind_kpis(self, data_values):
        """ Bind and filter KPI values from execution results.

        Parameters
        ----------
        data_values: list of DataValues
            A list of data values (usually from execution results).

        Returns
        -------
        data_values : list of DataValues
            The data values corresponding to the KPIs.
        """
        kpi_names = [kpi.name for kpi in self.kpis]

        kpi_results = [
            dv
            for kpi_name in kpi_names
            for dv in data_values
            if dv.name == kpi_name
        ]

        return kpi_results

    def verify(self):
        """ Verify the MCO model.

        Check that the MCO model:

        - has at least one parameter
        - has at least one KPI
        - has no parameter errors
        - has no KPI errors

        Returns
        -------
        errors : list of VerifierErrors
            The list of all detected errors in the MCO model.
        """
        errors = []

        if not self.parameters:
            errors.append(
                VerifierError(
                    subject=self,
                    global_error="The MCO has no defined parameters",
                )
            )

        if not self.kpis:
            errors.append(
                VerifierError(
                    subject=self, global_error="The MCO has no defined KPIs"
                )
            )

        for parameter in self.parameters:
            errors += parameter.verify()

        for kpi in self.kpis:
            errors += kpi.verify()

        return errors

    def create_start_event(self):
        """ Creates base event indicating the start of the MCO."""
        return MCOStartEvent(
            parameter_names=list(p.name for p in self.parameters),
            kpi_names=list(kpi.name for kpi in self.kpis),
        )

    def create_finish_event(self):
        """ Creates base event indicating the finished MCO."""
        return MCOFinishEvent()

    @classmethod
    def from_json(cls, factory, json_data):
        """ Instantiate an BaseMCOModel object from a `json_data`
        dictionary and the generating `factory` object.

        Parameters
        ----------
        factory: BaseMCOFactory
            Generating factory object
        json_data: dict
            Dictionary with an MCOModel  serialized data

        Returns
        ----------
        layer: BaseMCOModel
            BaseMCOModel instance with attributes values from
            the `json_data` dict
        """
        data = deepcopy(json_data)

        parameters = []
        for parameter_data in data["parameters"]:
            id = parameter_data["id"]
            parameter_factory = factory.parameter_factory_by_id(id)
            parameter = parameter_factory.model_class.from_json(
                parameter_factory, parameter_data["model_data"]
            )
            parameters.append(parameter)
        data["parameters"] = parameters

        data["kpis"] = [KPISpecification(**d) for d in data["kpis"]]

        mco_model = factory.create_model(data)
        return mco_model
