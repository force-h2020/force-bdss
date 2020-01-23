from copy import deepcopy
import json
import unittest

from traits.testing.api import UnittestTools

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.core.workflow import Workflow
from force_bdss.tests.probe_classes.data_source import ProbeDataSourceFactory
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.data_value import DataValue
from force_bdss.notification_listeners.base_notification_listener_model \
    import BaseNotificationListenerModel
from force_bdss.tests.probe_classes.factory_registry import (
    ProbeFactoryRegistry,
)
from force_bdss.tests.probe_classes.mco import ProbeMCOFactory
from force_bdss.tests.dummy_classes.factory_registry import (
    DummyFactoryRegistry,
)
from force_bdss.tests.dummy_classes.mco import DummyMCOParameter
from force_bdss.tests.dummy_classes.data_source import DummyDataSourceModel
from force_bdss.tests import fixtures


class TestWorkflow(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.registry = ProbeFactoryRegistry()
        self.plugin = self.registry.plugin

    def test_empty__getstate__(self):
        workflow = Workflow()
        state = workflow.__getstate__()
        self.assertDictEqual(
            state,
            {
                "mco_model": None,
                "execution_layers": [],
                "notification_listeners": [],
            },
        )

    def test_multilayer_execution(self):
        # The multilayer peforms the following execution
        # layer 0: in1 + in2   | in3 + in4
        #             res1          res2
        # layer 1:        res1 + res2
        #                    res3
        # layer 2:        res3 * res1
        #                     res4
        # layer 3:        res4 * res2
        #                     out1
        # Final result should be
        # out1 = ((in1 + in2 + in3 + in4) * (in1 + in2) * (in3 + in4)

        data_values = [
            DataValue(value=10, name="in1"),
            DataValue(value=15, name="in2"),
            DataValue(value=3, name="in3"),
            DataValue(value=7, name="in4"),
        ]

        def adder(model, parameters):

            first = parameters[0].value
            second = parameters[1].value
            return [DataValue(value=(first + second))]

        adder_factory = ProbeDataSourceFactory(
            self.plugin,
            input_slots_size=2,
            output_slots_size=1,
            run_function=adder,
        )

        def multiplier(model, parameters):
            first = parameters[0].value
            second = parameters[1].value
            return [DataValue(value=(first * second))]

        multiplier_factory = ProbeDataSourceFactory(
            self.plugin,
            input_slots_size=2,
            output_slots_size=1,
            run_function=multiplier,
        )

        mco_factory = ProbeMCOFactory(self.plugin)
        mco_model = mco_factory.create_model()
        parameter_factory = mco_factory.parameter_factories[0]

        mco_model.parameters = [
            parameter_factory.create_model({"name": "in1"}),
            parameter_factory.create_model({"name": "in2"}),
            parameter_factory.create_model({"name": "in3"}),
            parameter_factory.create_model({"name": "in4"}),
        ]
        mco_model.kpis = [KPISpecification(name="out1")]

        wf = Workflow(
            mco_model=mco_model,
            execution_layers=[
                ExecutionLayer(),
                ExecutionLayer(),
                ExecutionLayer(),
                ExecutionLayer(),
            ],
        )
        # Layer 0
        model = adder_factory.create_model()
        model.input_slot_info = [
            InputSlotInfo(name="in1"),
            InputSlotInfo(name="in2"),
        ]
        model.output_slot_info = [OutputSlotInfo(name="res1")]
        wf.execution_layers[0].data_sources.append(model)

        model = adder_factory.create_model()
        model.input_slot_info = [
            InputSlotInfo(name="in3"),
            InputSlotInfo(name="in4"),
        ]
        model.output_slot_info = [OutputSlotInfo(name="res2")]
        wf.execution_layers[0].data_sources.append(model)

        # layer 1
        model = adder_factory.create_model()
        model.input_slot_info = [
            InputSlotInfo(name="res1"),
            InputSlotInfo(name="res2"),
        ]
        model.output_slot_info = [OutputSlotInfo(name="res3")]
        wf.execution_layers[1].data_sources.append(model)

        # layer 2
        model = multiplier_factory.create_model()
        model.input_slot_info = [
            InputSlotInfo(name="res3"),
            InputSlotInfo(name="res1"),
        ]
        model.output_slot_info = [OutputSlotInfo(name="res4")]
        wf.execution_layers[2].data_sources.append(model)

        # layer 3
        model = multiplier_factory.create_model()
        model.input_slot_info = [
            InputSlotInfo(name="res4"),
            InputSlotInfo(name="res2"),
        ]
        model.output_slot_info = [OutputSlotInfo(name="out1")]
        wf.execution_layers[3].data_sources.append(model)

        kpi_results = wf.execute(data_values)
        self.assertEqual(1, len(kpi_results))
        self.assertEqual(8750, kpi_results[0].value)

    def test_kpi_specification_adherence(self):
        # Often the user may only wish to treat a subset of DataSource
        # output slots as KPIs. This test makes sure they get what they
        # ask for!

        # keep input DataValues constant
        data_values = [
            DataValue(value=99, name="in1"),
            DataValue(value=1, name="in2"),
        ]

        # dummy addition DataSource(a, b) that also returns its inputs
        # [a, b, a+b]
        def adder(model, parameters):
            first = parameters[0].value
            second = parameters[1].value
            return [
                DataValue(value=first),
                DataValue(value=second),
                DataValue(value=(first + second)),
            ]

        adder_factory = ProbeDataSourceFactory(
            self.plugin,
            input_slots_size=2,
            output_slots_size=3,
            run_function=adder,
        )

        mco_factory = ProbeMCOFactory(self.plugin)
        parameter_factory = mco_factory.parameter_factories[0]
        mco_model = mco_factory.create_model()

        # DataSourceModel stats constant throughout
        model = adder_factory.create_model()
        model.input_slot_info = [
            InputSlotInfo(name="in1"),
            InputSlotInfo(name="in2"),
        ]
        model.output_slot_info = [
            OutputSlotInfo(name="out1"),
            OutputSlotInfo(name="out2"),
            OutputSlotInfo(name="out3"),
        ]

        # test Parameter and KPI spec that follows DataSource slots
        # exactly
        mco_model.parameters = [
            parameter_factory.create_model({"name": "in1"}),
            parameter_factory.create_model({"name": "in2"}),
        ]
        mco_model.kpis = [
            KPISpecification(name="out1"),
            KPISpecification(name="out2"),
            KPISpecification(name="out3"),
        ]
        # need to make a new workflow for each KPISpecification
        wf = Workflow(mco_model=mco_model, execution_layers=[ExecutionLayer()])
        wf.execution_layers[0].data_sources.append(model)
        kpi_results = wf.execute(data_values)
        self.assertEqual(len(kpi_results), 3)
        self.assertEqual(kpi_results[0].value, 99)
        self.assertEqual(kpi_results[1].value, 1)
        self.assertEqual(kpi_results[2].value, 100)
        self.assertEqual(kpi_results[0].name, "out1")
        self.assertEqual(kpi_results[1].name, "out2")
        self.assertEqual(kpi_results[2].name, "out3")

        # now test all possible combinations of KPISpecification, including
        # those with KPIs repeated, and empty KPI specification
        import itertools

        out_options = [("out1", 99), ("out2", 1), ("out3", 100)]
        for num_outputs in range(len(out_options) + 2, 0, -1):
            for spec in itertools.permutations(out_options, r=num_outputs):
                mco_model.kpis = [
                    KPISpecification(name=opt[0]) for opt in spec
                ]

                wf = Workflow(
                    mco_model=mco_model, execution_layers=[ExecutionLayer()]
                )
                wf.execution_layers[0].data_sources.append(model)
                kpi_results = wf.execute(data_values)
                self.assertEqual(len(kpi_results), num_outputs)

                for i in range(num_outputs):
                    self.assertEqual(kpi_results[i].name, spec[i][0])
                    self.assertEqual(kpi_results[i].value, spec[i][1])

    def test_from_json(self):
        registry = DummyFactoryRegistry()
        json_path = fixtures.get("test_workflow_reader.json")
        with open(json_path) as f:
            data = json.load(f)
        wf = Workflow.from_json(registry, data["workflow"])
        workflow_state = wf.__getstate__()
        self.assertDictEqual(
            workflow_state,
            {
                "mco_model": {
                    "id": "force.bdss.enthought.plugin.test.v0.factory."
                    "dummy_mco",
                    "model_data": {
                        "parameters": [
                            {
                                "id": "force.bdss.enthought.plugin."
                                "test.v0.factory."
                                "dummy_mco.parameter.dummy_mco_parameter",
                                "model_data": {"x": 0, "name": "", "type": ""},
                            }
                        ],
                        "kpis": [],
                    },
                },
                "notification_listeners": [
                    {
                        "id": "force.bdss.enthought.plugin.test.v0.factory."
                        "dummy_notification_listener",
                        "model_data": {},
                    }
                ],
                "execution_layers": [
                    {
                        "data_sources": [
                            {
                                "id": "force.bdss.enthought.plugin.test.v0."
                                "factory.dummy_data_source",
                                "model_data": {
                                    "input_slot_info": [
                                        {
                                            "name": "input_slot_name",
                                            "source": "Environment",
                                        }
                                    ],
                                    "output_slot_info": [
                                        {"name": "output_slot_name"}
                                    ],
                                },
                            }
                        ]
                    }
                ],
            },
        )

    def test_persistent_wfdata(self):
        registry = DummyFactoryRegistry()
        json_path = fixtures.get("test_workflow_reader.json")
        with open(json_path) as f:
            data = json.load(f)
        reference_data = deepcopy(data)
        _ = Workflow.from_json(registry, data["workflow"])
        self.assertDictEqual(data, reference_data)

    def test__extract_mco_model(self):
        registry = DummyFactoryRegistry()
        with open(fixtures.get("test_workflow_reader.json")) as f:
            data = json.load(f)

        workflow_data = data["workflow"]
        mco_model = Workflow._extract_mco_model(registry, workflow_data)

        mco_factory = registry.mco_factories[0]
        expected_mco_model = mco_factory.model_class
        self.assertIsInstance(mco_model, expected_mco_model)
        self.assertEqual(0, len(mco_model.kpis))
        self.assertEqual(1, len(mco_model.parameters))
        self.assertIsInstance(mco_model.parameters[0], DummyMCOParameter)

    def test__extract_execution_layers(self):
        registry = DummyFactoryRegistry()
        with open(fixtures.get("test_workflow_reader.json")) as f:
            data = json.load(f)

        workflow_data = data["workflow"]
        exec_layers = Workflow._extract_execution_layers(
            registry, workflow_data
        )
        self.assertEqual(1, len(exec_layers))
        self.assertIsInstance(exec_layers[0], ExecutionLayer)

        self.assertEqual(1, len(exec_layers[0].data_sources))
        data_source = exec_layers[0].data_sources[0]
        self.assertIsInstance(data_source, DummyDataSourceModel)

        input_slots = data_source.input_slot_info
        self.assertEqual(1, len(input_slots))
        self.assertIsInstance(input_slots[0], InputSlotInfo)
        self.assertEqual("input_slot_name", input_slots[0].name)

        output_slots = data_source.output_slot_info
        self.assertEqual(1, len(output_slots))
        self.assertIsInstance(output_slots[0], OutputSlotInfo)
        self.assertEqual("output_slot_name", output_slots[0].name)

    def test__extract_notification_listeners(self):
        registry = DummyFactoryRegistry()
        with open(fixtures.get("test_workflow_reader.json")) as f:
            data = json.load(f)

        workflow_data = data["workflow"]
        listeners = Workflow._extract_notification_listeners(
            registry, workflow_data
        )
        self.assertEqual(1, len(listeners))
        self.assertIsInstance(listeners[0], BaseNotificationListenerModel)
