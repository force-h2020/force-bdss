import json
import unittest

from six import StringIO

from force_bdss.data_sources.base_data_source_factory import \
    BaseDataSourceFactory
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.data_sources.i_data_source_factory import IDataSourceFactory
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

        datasource_factory = BaseDataSourceFactory(
            id=factory_id("enthought", "mock2"), plugin=None)

        self.mock_registry.data_source_factory_by_id = mock.Mock(
            return_value=datasource_factory
        )

    def test_write(self):
        wfwriter = WorkflowWriter()
        fp = StringIO()
        wf = self._create_mock_workflow()
        wfwriter.write(wf, fp)
        result = json.loads(fp.getvalue())
        self.assertIn("version", result)
        self.assertIn("workflow", result)
        self.assertIn("mco", result["workflow"])
        self.assertIn("execution_layers", result["workflow"])
        self.assertIn("kpi_calculators", result["workflow"])

    def test_write_and_read(self):
        wfwriter = WorkflowWriter()
        fp = StringIO()
        wf = self._create_mock_workflow()
        wfwriter.write(wf, fp)
        fp.seek(0)
        wfreader = WorkflowReader(self.mock_registry)
        wf_result = wfreader.read(fp)
        self.assertEqual(wf_result.mco.factory.id,
                         wf.mco.factory.id)
        self.assertEqual(len(wf_result.execution_layers), 2)
        self.assertEqual(len(wf_result.execution_layers[0]), 2)
        self.assertEqual(len(wf_result.execution_layers[1]), 1)

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
        wf.execution_layers = [
            [
                BaseDataSourceModel(mock.Mock(spec=IDataSourceFactory,
                                    id=factory_id("enthought", "mock2"))),
                BaseDataSourceModel(mock.Mock(spec=IDataSourceFactory,
                                    id=factory_id("enthought", "mock2"))),
            ],
            [
                BaseDataSourceModel(mock.Mock(spec=IDataSourceFactory,
                                    id=factory_id("enthought", "mock2")))
            ]
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
