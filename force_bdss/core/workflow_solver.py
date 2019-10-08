import logging
import subprocess

from traits.api import (
    HasStrictTraits, Instance, Unicode, Enum, List, Float,
    provides
)

from force_bdss.core.data_value import DataValue
from force_bdss.core.workflow import Workflow

from .i_solver import ISolver

log = logging.getLogger(__name__)


@provides(ISolver)
class WorkflowSolver(HasStrictTraits):
    """A class that can be passed into a BaseMCO to evaluate the
    state of a system described by a Workflow object a given set of
    parameter values. Contains all information required to either
    perform this locally, or call another BDSS process to do so."""

    #: The workflow instance.
    workflow = Instance(Workflow)

    #: The path to the workflow file.
    workflow_filepath = Unicode()

    #: Values for each parameter in thw workflow to calculate a
    #: single point
    parameter_values = List(Float)

    #: The path to the force_bdss executable
    executable_path = Unicode()

    #: Mode of evaluation, either running internally on this process
    #: or spawning another process using subprocess
    mode = Enum('Internal', 'Subprocess')

    def _internal_solve(self):
        """Executes the workflow using the given parameter values
        running on the internal process"""

        data_values = [
            DataValue(type=parameter.type,
                      name=parameter.name,
                      value=value)
            for parameter, value in zip(
                self.workflow.mco.parameter, self.parameter_values)]

        kpi_results = self.workflow.execute(data_values)

        return kpi_results

    def _subprocess_solve(self):
        """Executes the workflow using the given parameter values
        running on an external process via the subprocess library."""

        # This command calls a force_bdss executable on another process
        # to evaluate the same workflow at a state determined by the
        # parameter values. A BaseMCOCommunicator will be needed to be
        # defined in the workflow to receive the data and send back values
        # corresponding to each KPI via the command line.
        cmd = [self.executable_path,
               "--logfile",
               "bdss.log",
               "--evaluate",
               self.workflow_filepath]

        log.info("Spawning subprocess: {}".format(cmd))
        ps = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        # Converts the parameter values to a string to send via subprocess
        string_values = [str(v) for v in self.parameter_values]
        log.info("Sending values: {}".format(string_values))
        out = ps.communicate(" ".join(string_values).encode("utf-8"))

        # Converts an incoming string of KPI values into floats
        kpi_values = [float(x) for x in out[0].decode("utf-8").split()]
        log.info("Received values: {}".format(kpi_values))

        kpi_results = [
            DataValue(type=kpi.type,
                      name=kpi.name,
                      value=value)
            for kpi, value in zip(
                self.workflow.mco.kpis, kpi_values)]

        return kpi_results

    def solve(self, parameter_values):
        """Public method to evaluate the workflow at a given set of
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

        self.parameter_values = parameter_values

        if self.mode == 'Internal':
            return self._internal_solve()

        elif self.mode == 'Subprocess':
            return self._subprocess_solve()
