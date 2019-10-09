import logging

from traits.api import Interface, Instance

from .base_mco_model import BaseMCOModel

log = logging.getLogger(__name__)


class IEvaluator(Interface):
    """Class that is used as a bridge between the BDSS application and
    MCO runner. It can be passed in as an argument to a MCO run and
    used to evaluate the state of a system for a given set of
    parameters, returning a set of KPIs. This avoids the need for the
    MCO to obtain any information regarding the Envisage application."""

    #: An instance of the MCO model information
    mco_model = Instance(BaseMCOModel)

    def evaluate(self, parameter_values):
        """Public method to evaluate the system at a given set of
        MCO parameter values

        Parameters
        ----------
        parameter_values: list
            List of values to assign to each BaseMCOParameter defined
            in the workflow

        Returns
        -------
        kpi_results: list
            List of values corresponding to each MCO KPI in the
            workflow
        """
