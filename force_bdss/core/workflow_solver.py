import os
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

    #: The path to the force_bdss executable
    executable_path = Unicode()

    #: Mode of evaluation, either running internally on this process
    #: or spawning another process using subprocess
    mode = Enum('Internal', 'Subprocess')

    def _internal_solve(self, parameter_values):
        """Executes the workflow using the given parameter values
        running on the internal process"""

        data_values = [
            DataValue(type=parameter.type,
                      name=parameter.name,
                      value=value)
            for parameter, value in zip(
                self.workflow.mco.parameters, parameter_values)]

        kpi_results = self.workflow.execute(data_values)

        return kpi_results

    def _call_subprocess(self, command, user_input):
        """Calls a subprocess to perform a command with parsed
        user_input"""

        log.info("Spawning subprocess: {}".format(command))

        # Setting ETS_TOOLKIT=null before executing bdss prevents it
        # from trying to create GUI every call, giving reducing the
        # overhead by a factor of 2.
        env = {**os.environ, "ETS_TOOLKIT": "null"}

        # Spawn the single point evaluation, which is the bdss itself
        # with the option evaluate.
        # We pass the specific parameter values via stdin, and read
        # the result via stdout.
        ps = subprocess.Popen(
            command,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        log.info("Sending values: {}".format(user_input))
        stdout, stderr = ps.communicate(" ".join(user_input).encode("utf-8"))

        return stdout

    def _subprocess_solve(self, parameter_values):
        """Executes the workflow using the given parameter values
        running on an external process via the subprocess library.
        Values for each parameter in thw workflow to calculate a
        single point
        """

        # This command calls a force_bdss executable on another process
        # to evaluate the same workflow at a state determined by the
        # parameter values. A BaseMCOCommunicator will be needed to be
        # defined in the workflow to receive the data and send back values
        # corresponding to each KPI via the command line.
        command = [self.executable_path,
                   "--logfile",
                   "bdss.log",
                   "--evaluate",
                   self.workflow_filepath]

        # Converts the parameter values to a string to send via
        # subprocess
        string_values = [str(v) for v in parameter_values]

        # Call subprocess to perform executable with user input
        stdout = self._call_subprocess(command, string_values)

        # Decode stdout into KPI float values
        kpi_values = [float(x) for x in stdout.decode("utf-8").split()]

        # Convert values into DataValues
        kpi_results = [
            DataValue(name=kpi.name,
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

        if self.mode == 'Internal':
            return self._internal_solve(parameter_values)

        elif self.mode == 'Subprocess':
            try:
                return self._subprocess_solve(parameter_values)
            except Exception:
                message = (
                    'Subprocess mode in a WorkflowSolver failed '
                    'to run. This is likely due to a error in the '
                    'BaseMCOCommunicator assigned to {}.'.format(
                        self.workflow.mco.factory.__class__)
                )
                log.exception(message)
                raise RuntimeError(message)
