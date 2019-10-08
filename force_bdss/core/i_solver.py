import logging

from traits.api import Interface

log = logging.getLogger(__name__)


class ISolver(Interface):
    """Class that is used as a bridge between the BDSS application and
    MCO runner. It can be passed in as an argument to a MCO run and
    used to evaluate the state of a system for a given set of
    parameters, returning a set of KPIs. This avoids the need for the
    MCO to obtain any information regarding the Envisage application."""

    def solve(self, parameter_values):
        """Public method to evaluate the system at a given set of
        MCO parameter values

        Parameters
        ----------
        parameter_values: List(Float)
            List of values to assign to each BaseMCOParameter defined
            in the workflow

        Returns
        -------
        kpi_results: List(DataValue)
            List of DataValues corresponding to each MCO KPI in the
            workflow
        """
