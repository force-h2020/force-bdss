from unittest import TestCase, mock

from force_bdss.tests import fixtures
from force_bdss.tests.probe_classes.workflow_file import (
    ProbeWorkflowFile
)

from .. data_value import DataValue
from .. workflow import Workflow
from .. workflow_solver import WorkflowSolver


class TestWorkflowSolver(TestCase):

    def setUp(self):
        file_path = "test_probe.json"
        workflow_file = ProbeWorkflowFile(
            path=fixtures.get("test_probe.json")
        )
        workflow_file.read()
        self.solver = WorkflowSolver(
            workflow=workflow_file.workflow,
            workflow_filepath=file_path
        )
        self.mock_process = mock.Mock()
        self.mock_process.communicate = mock.Mock(
            return_value=(b"2", b"1 0")
        )

    def test_empty_init(self):

        solver = WorkflowSolver()
        self.assertIsNone(solver.workflow)
        self.assertEqual('', solver.workflow_filepath)
        self.assertListEqual([], solver.parameter_values)
        self.assertEqual('', solver.executable_path)
        self.assertEqual('Internal', solver.mode)

    def test_init(self):

        self.assertIsInstance(self.solver.workflow, Workflow)
        self.assertEqual("test_probe.json", self.solver.workflow_filepath)
        self.assertListEqual([], self.solver.parameter_values)
        self.assertEqual('', self.solver.executable_path)
        self.assertEqual('Internal', self.solver.mode)

    def test__internal_solve(self):

        self.solver.parameter_values = [1.0]
        kpi_results = self.solver._internal_solve()

        self.assertEqual(1, len(kpi_results))
        self.assertIsInstance(kpi_results[0], DataValue)

    def test___call_subprocess(self):

        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = self.mock_process
            stdout = self.solver._call_subprocess(
                'echo', ['1.0']
            )
        self.assertEqual(b'2', stdout)

    def test__subprocess_solve(self):

        self.solver.parameter_values = [1.0]
        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = self.mock_process
            kpi_results = self.solver._subprocess_solve()

        self.assertEqual(1, len(kpi_results))
        self.assertIsInstance(kpi_results[0], DataValue)
        self.assertEqual(2, kpi_results[0].value)

    def test_solve_missing_mco_communicator(self):

        self.solver.mode = "Subprocess"
        with self.assertRaisesRegex(
                RuntimeError,
                'Subprocess mode in a WorkflowSolver failed '
                'to run. This is likely due to a error in the '
                'BaseMCOCommunicator assigned to '
                "<class 'force_bdss.tests.probe_classes.mco."
                "ProbeMCOFactory'>."):
            self.solver.solve([1.0])

    def test_solve(self):

        kpi_results = self.solver.solve([1.0])
        self.assertEqual(1, len(kpi_results))
        self.assertIsInstance(kpi_results[0], DataValue)
        self.assertIsNone(kpi_results[0].value)

        self.solver.mode = "Subprocess"
        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = self.mock_process
            kpi_results = self.solver.solve([1.0])

        self.assertEqual(1, len(kpi_results))
        self.assertIsInstance(kpi_results[0], DataValue)
        self.assertEqual(2, kpi_results[0].value)
