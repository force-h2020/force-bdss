import unittest

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.core.verifier import verify_workflow
from force_bdss.core.workflow import Workflow
from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.tests.dummy_classes.extension_plugin import \
    DummyExtensionPlugin


class TestVerifier(unittest.TestCase):
    def setUp(self):
        self.plugin = DummyExtensionPlugin()
        self.workflow = Workflow()

    def test_empty_workflow(self):
        wf = self.workflow
        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[0].subject, wf)
        self.assertIn("no MCO", errors[0].error)

        self.assertEqual(errors[1].subject, wf)
        self.assertIn("no execution layers", errors[1].error)

    def test_no_mco_parameters(self):
        wf = self.workflow
        wf.mco = self.plugin.mco_factories[0].create_model()

        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[0].subject, wf.mco)
        self.assertIn("no defined parameters", errors[0].error)

    def test_parameters_empty_names(self):
        wf = self.workflow
        mco_factory = self.plugin.mco_factories[0]
        wf.mco = mco_factory.create_model()
        parameter_factory = mco_factory.parameter_factories()[0]
        wf.mco.parameters.append(parameter_factory.create_model())

        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[0].subject, wf.mco.parameters[0])
        self.assertIn("empty name", errors[0].error)
        self.assertEqual(errors[1].subject, wf.mco.parameters[0])
        self.assertIn("empty type", errors[1].error)

    def test_kpis_empty_names(self):
        wf = self.workflow
        mco_factory = self.plugin.mco_factories[0]
        wf.mco = mco_factory.create_model()
        kpi = KPISpecification(name='', objective='MINIMISE')
        wf.mco.kpis.append(kpi)

        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[1].subject, wf.mco.kpis[0])
        self.assertIn("KPI 0 has empty name", errors[1].error)

    def test_empty_execution_layer(self):
        wf = self.workflow
        mco_factory = self.plugin.mco_factories[0]
        wf.mco = mco_factory.create_model()
        parameter_factory = mco_factory.parameter_factories()[0]
        wf.mco.parameters.append(parameter_factory.create_model())
        wf.mco.parameters[0].name = "name"
        wf.mco.parameters[0].type = "type"

        layer = ExecutionLayer()
        wf.execution_layers.append(layer)
        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].subject, wf.execution_layers[0])
        self.assertIn("Layer 0 has no data sources", errors[0].error)

    def test_data_sources(self):
        wf = self.workflow
        mco_factory = self.plugin.mco_factories[0]
        wf.mco = mco_factory.create_model()
        parameter_factory = mco_factory.parameter_factories()[0]
        wf.mco.parameters.append(parameter_factory.create_model())
        wf.mco.parameters[0].name = "name"
        wf.mco.parameters[0].type = "type"

        layer = ExecutionLayer()
        wf.execution_layers.append(layer)
        ds_factory = self.plugin.data_source_factories[0]
        ds_model = ds_factory.create_model()
        layer.data_sources.append(ds_model)

        errors = verify_workflow(wf)
        self.assertEqual(errors[0].subject, ds_model)
        self.assertIn("Missing input slot name assignment", errors[0].error)

        ds_model.input_slot_info.append(
            InputSlotInfo(name="name")
        )

        errors = verify_workflow(wf)
        self.assertEqual(errors[0].subject, ds_model)
        self.assertIn("Missing output slot name assignment", errors[0].error)

        ds_model.output_slot_info.append(
            OutputSlotInfo(name="name")
        )

        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 0)

        ds_model.input_slot_info[0].name = ''
        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 1)
        self.assertIn("Undefined name for input parameter", errors[0].error)

        ds_model.output_slot_info[0].name = ''
        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 2)
        self.assertIn("Undefined name for output parameter", errors[1].error)
