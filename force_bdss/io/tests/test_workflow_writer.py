import json
import unittest

from io import StringIO
from unittest import mock

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.io.workflow_reader import WorkflowReader
from force_bdss.tests.dummy_classes.factory_registry_plugin import \
    DummyFactoryRegistryPlugin

from force_bdss.io.workflow_writer import WorkflowWriter, traits_to_dict,\
    pop_recursive, pop_dunder_recursive
from force_bdss.core.workflow import Workflow
from force_bdss.core.input_slot_info import InputSlotInfo


class TestWorkflowWriter(unittest.TestCase):
    def setUp(self):
        self.registry = DummyFactoryRegistryPlugin()
        self.mco_factory = self.registry.mco_factories[0]
        self.mco_parameter_factory = self.mco_factory.parameter_factories[0]
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

    def test_traits_to_dict(self):

        wfwriter = WorkflowWriter()
        wf = self._create_workflow()
        exec_layer = wf.execution_layers[0]
        exec_layer.data_sources[0].input_slot_info = [InputSlotInfo()]
        slotdata = exec_layer.data_sources[0].input_slot_info[0].__getstate__()
        self.assertTrue("__traits_version__" in slotdata)
        # Calls traits_to_dict for each data source
        datastore_list = wfwriter._execution_layer_data(exec_layer)
        new_slotdata = datastore_list[0]['model_data']['input_slot_info']
        self.assertTrue("__traits_version__" not in new_slotdata)

        test_dictionary = {'K1': {'K1': 'V1', 'K2': 'V2', 'K3': 'V3'},
                           'K2': ['V1', 'V2', {'K1': 'V1', 'K2': 'V2',
                                               'K3': 'V3'}],
                           'K3': 'V3',
                           'K4': ('V1', {'K3': 'V3'},)}

        result_dictionary = {'K1': {'K1': 'V1', 'K2': 'V2', },
                             'K2': ['V1', 'V2', {'K1': 'V1', 'K2': 'V2', }],
                             'K4': ('V1', {},)}

        test_result_dictionary = pop_recursive(test_dictionary, 'K3')
        self.assertEqual(test_result_dictionary, result_dictionary)

    def test_dunder_recursive(self):
        test_dict = {
            '__traits_version__': '4.6.0',
            'some_important_data':
                {'__traits_version__': '4.6.0', 'value': 10},
            '_some_private_data':
                {'__instance_traits__': ['yes', 'some']},
            '___':
                {'__': 'a', 'foo': 'bar'}
        }
        expected = {'some_important_data': {'value': 10},
                    '_some_private_data': {}}
        self.assertEqual(pop_dunder_recursive(test_dict), expected)
