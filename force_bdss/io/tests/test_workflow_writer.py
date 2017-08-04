import json
import unittest

from six import StringIO

from force_bdss.factory_registry_plugin import FactoryRegistryPlugin
from force_bdss.io.workflow_reader import WorkflowReader
from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.ids import factory_id, mco_parameter_id
from force_bdss.io.workflow_writer import WorkflowWriter
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.mco.i_mco_factory import IMCOFactory
from force_bdss.core.workflow import Workflow


class TestWorkflowWriter(unittest.TestCase):
    def setUp(self):
        self.mock_registry = mock.Mock(spec=FactoryRegistryPlugin)
        mock_mco_factory = mock.Mock(spec=IMCOFactory,
                                     id=factory_id("enthought", "mock"))
        mock_mco_model = mock.Mock(
            spec=BaseMCOModel,
            factory=mock_mco_factory
        )
        mock_mco_factory.create_model = mock.Mock(
            return_value=mock_mco_model
        )
        self.mock_registry.mco_factory_by_id = mock.Mock(
            return_value=mock_mco_factory)

    def test_write(self):
        wfwriter = WorkflowWriter()
        fp = StringIO()
        wf = self._create_mock_workflow()
        wfwriter.write(wf, fp)
        result = json.loads(fp.getvalue())
        self.assertIn("version", result)
        self.assertIn("workflow", result)
        self.assertIn("mco", result["workflow"])
        self.assertIn("data_sources", result["workflow"])
        self.assertIn("kpi_calculators", result["workflow"])

    def test_write_and_read(self):
        wfwriter = WorkflowWriter()
        fp = StringIO()
        wf = self._create_mock_workflow()
        wfwriter.write(wf, fp)
        print(fp.getvalue())
        fp.seek(0)
        wfreader = WorkflowReader(self.mock_registry)
        wf_result = wfreader.read(fp)
        self.assertEqual(wf_result.mco.factory.id,
                         wf.mco.factory.id)

    def _create_mock_workflow(self):
        wf = Workflow()
        wf.mco = BaseMCOModel(
            mock.Mock(
                spec=IMCOFactory,
                id=factory_id("enthought", "mock")))
        wf.mco.parameters = [
            BaseMCOParameter(
                factory=mock.Mock(
                    spec=BaseMCOParameterFactory,
                    id=mco_parameter_id("enthought", "mock", "mock")
                )
            )
        ]
        return wf

    def test_write_and_read_empty_workflow(self):
        wf = Workflow()
        wfwriter = WorkflowWriter()
        fp = StringIO()
        wfwriter.write(wf, fp)
        fp.seek(0)
        wfreader = WorkflowReader(self.mock_registry)
        wf_result = wfreader.read(fp)
        self.assertIsNone(wf_result.mco)
