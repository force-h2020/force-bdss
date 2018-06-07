import json
import unittest

from six import StringIO
try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.io.workflow_reader import WorkflowReader
from force_bdss.tests.dummy_classes.factory_registry_plugin import \
    DummyFactoryRegistryPlugin

from force_bdss.io.workflow_writer import WorkflowWriter, traits_to_dict
from force_bdss.core.workflow import Workflow


class TestWorkflowWriter(unittest.TestCase):
    def setUp(self):
        self.registry = DummyFactoryRegistryPlugin()
        self.mco_factory = self.registry.mco_factories[0]
        self.mco_parameter_factory = self.mco_factory.parameter_factories()[0]
        self.data_source_factory = self.registry.data_source_factories[0]

    def test_write(self):
        wfwriter = WorkflowWriter()
        fp = StringIO()
        wf = self._create_workflow()
        wfwriter.write(wf, fp)
        result = json.loads(fp.getvalue())
        self.assertIn("version", result)
        self.assertIn("workflow", result)
        self.assertIn("mco", result["workflow"])
        self.assertIn("execution_layers", result["workflow"])

    def test_write_and_read(self):
        wfwriter = WorkflowWriter()
        fp = StringIO()
        wf = self._create_workflow()
        wfwriter.write(wf, fp)
        fp.seek(0)
        wfreader = WorkflowReader(self.registry)
        wf_result = wfreader.read(fp)
        self.assertEqual(wf_result.mco.factory.id,
                         wf.mco.factory.id)
        self.assertEqual(len(wf_result.execution_layers), 2)
        self.assertEqual(
            len(wf_result.execution_layers[0].data_sources), 2)
        self.assertEqual(
            len(wf_result.execution_layers[1].data_sources), 1)

    def _create_workflow(self):
        wf = Workflow()

        wf.mco = self.mco_factory.create_model()
        wf.mco.parameters = [
            self.mco_parameter_factory.create_model()
        ]
        wf.mco.kpis = [
            KPISpecification()
        ]
        wf.execution_layers = [
            ExecutionLayer(data_sources=[
                self.data_source_factory.create_model(),
                self.data_source_factory.create_model(),
            ]),
            ExecutionLayer(data_sources=[
                self.data_source_factory.create_model(),
            ])
        ]
        return wf

    def test_write_and_read_empty_workflow(self):
        wf = Workflow()
        wfwriter = WorkflowWriter()
        fp = StringIO()
        wfwriter.write(wf, fp)
        fp.seek(0)
        wfreader = WorkflowReader(self.registry)
        wf_result = wfreader.read(fp)
        self.assertIsNone(wf_result.mco)

    def test_traits_to_dict_no_version(self):
        mock_traits = mock.Mock()
        mock_traits.__getstate__ = mock.Mock(return_value={"foo": "bar"})

        self.assertEqual(traits_to_dict(mock_traits), {"foo": "bar"})
