import unittest
import json
from six import StringIO

from force_bdss.bundle_registry_plugin import BundleRegistryPlugin
from force_bdss.io.workflow_reader import WorkflowReader
from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory
from force_bdss.mco.parameters.mco_parameter_factory_registry import \
    MCOParameterFactoryRegistry

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.ids import bundle_id, mco_parameter_id
from force_bdss.io.workflow_writer import WorkflowWriter
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.mco.i_mco_bundle import IMCOBundle
from force_bdss.workspecs.workflow import Workflow


class TestWorkflowWriter(unittest.TestCase):
    def setUp(self):
        self.mock_registry = mock.Mock(spec=BundleRegistryPlugin)
        mock_mco_bundle = mock.Mock(spec=IMCOBundle,
                                    id=bundle_id("enthought", "mock"))
        mock_mco_model = mock.Mock(
            spec=BaseMCOModel,
            bundle=mock_mco_bundle
        )
        mock_mco_bundle.create_model = mock.Mock(
            return_value=mock_mco_model
        )
        self.mock_registry.mco_bundle_by_id = mock.Mock(
            return_value=mock_mco_bundle)

        self.mock_mco_parameter_registry = mock.Mock(
            spec=MCOParameterFactoryRegistry)

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
        fp.seek(0)
        wfreader = WorkflowReader(self.mock_registry,
                                  self.mock_mco_parameter_registry)
        wf_result = wfreader.read(fp)
        self.assertEqual(wf_result.mco.bundle.id,
                         wf.mco.bundle.id)

    def _create_mock_workflow(self):
        wf = Workflow()
        wf.mco = BaseMCOModel(
            mock.Mock(
                spec=IMCOBundle,
                id=bundle_id("enthought", "mock")))
        wf.mco.parameters = [
            BaseMCOParameter(
                factory=mock.Mock(
                    spec=BaseMCOParameterFactory,
                    id=mco_parameter_id("enthought", "mock")
                )
            )
        ]
        return wf
