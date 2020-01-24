import json
import unittest

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.io.workflow_reader import WorkflowReader
from force_bdss.tests.dummy_classes.factory_registry import (
    DummyFactoryRegistry,
)

from force_bdss.io.workflow_writer import (
    WorkflowWriter,
)
from force_bdss.core.base_model import pop_recursive, pop_dunder_recursive
from force_bdss.core.workflow import Workflow
from force_bdss.core.input_slot_info import InputSlotInfo


class TestWorkflowWriter(unittest.TestCase):
    def setUp(self):
        self.registry = DummyFactoryRegistry()
        self.mco_factory = self.registry.mco_factories[0]
        self.mco_parameter_factory = self.mco_factory.parameter_factories[0]
        self.data_source_factory = self.registry.data_source_factories[0]

    def sample_workflow(self):
        wf = Workflow()

        wf.mco_model = self.mco_factory.create_model()
        wf.mco_model.parameters = [self.mco_parameter_factory.create_model()]
        wf.mco_model.kpis = [KPISpecification()]
        wf.execution_layers = [
            ExecutionLayer(
                data_sources=[
                    self.data_source_factory.create_model(),
                    self.data_source_factory.create_model(),
                ]
            ),
            ExecutionLayer(
                data_sources=[self.data_source_factory.create_model()]
            ),
        ]
        return wf

    def test_write(self):
        wfwriter = WorkflowWriter()
        workflow = self.sample_workflow()

        filename = "tmp.json"
        wfwriter.write(workflow, filename)
        with open(filename) as f:
            result = json.load(f)

        self.assertIn("version", result)
        self.assertIn("workflow", result)
        self.assertIn("mco_model", result["workflow"])
        self.assertIn("execution_layers", result["workflow"])

    def test_write_and_read(self):
        wfwriter = WorkflowWriter()
        workflow = self.sample_workflow()

        filename = "tmp.json"
        wfwriter.write(workflow, filename)

        wfreader = WorkflowReader(self.registry)
        wf_result = wfreader.read(filename)
        self.assertEqual(
            wf_result.mco_model.factory.id, workflow.mco_model.factory.id
        )
        self.assertEqual(len(wf_result.execution_layers), 2)
        self.assertEqual(len(wf_result.execution_layers[0].data_sources), 2)
        self.assertEqual(len(wf_result.execution_layers[1].data_sources), 1)

    def test_get_workflow_data(self):
        wfwriter = WorkflowWriter()
        workflow = Workflow()
        self.assertDictEqual(
            wfwriter.get_workflow_data(workflow),
            workflow.__getstate__(),
        )

    def test_write_and_read_empty_workflow(self):
        workflow = Workflow()
        wfwriter = WorkflowWriter()

        filename = "tmp.json"
        wfwriter.write(workflow, filename)

        wfreader = WorkflowReader(self.registry)
        wf_result = wfreader.read(filename)
        self.assertIsNone(wf_result.mco_model)

    def test_traits_to_dict(self):
        wf = self.sample_workflow()
        exec_layer = wf.execution_layers[0]
        exec_layer.data_sources[0].input_slot_info = [InputSlotInfo()]

        datastore_list = exec_layer.__getstate__()
        new_slotdata = datastore_list["data_sources"][0]["model_data"][
            "input_slot_info"
        ]
        self.assertNotIn("__traits_version__", new_slotdata)


class TestDictUtils(unittest.TestCase):
    def test_dunder_recursive(self):
        test_dict = {
            "__traits_version__": "4.6.0",
            "some_important_data": {
                "__traits_version__": "4.6.0",
                "value": 10,
            },
            "_some_private_data": {"__instance_traits__": ["yes", "some"]},
            "___": {"__": "a", "foo": "bar"},
            "list_of_dicts": [
                {"__bad_key__": "bad", "good_key": "good"},
                {"also_good_key": "good"},
            ],
        }
        expected = {
            "some_important_data": {"value": 10},
            "_some_private_data": {},
            "list_of_dicts": [{"good_key": "good"}, {"also_good_key": "good"}],
        }
        self.assertEqual(pop_dunder_recursive(test_dict), expected)

    def test_pop_recursive(self):
        test_dictionary = {
            "K1": {"K1": "V1", "K2": "V2", "K3": "V3"},
            "K2": ["V1", "V2", {"K1": "V1", "K2": "V2", "K3": "V3"}],
            "K3": "V3",
            "K4": ("V1", {"K3": "V3"}),
        }

        result_dictionary = {
            "K1": {"K1": "V1", "K2": "V2"},
            "K2": ["V1", "V2", {"K1": "V1", "K2": "V2"}],
            "K4": ("V1", {}),
        }

        test_result_dictionary = pop_recursive(test_dictionary, "K3")
        self.assertEqual(test_result_dictionary, result_dictionary)

        small_dict = {"key": "value"}
        missing_key = "another_key"
        self.assertDictEqual(
            pop_recursive(small_dict, missing_key), small_dict
        )
