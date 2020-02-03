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
        self.assertIn("no MCO", errors[0].local_error)

        self.assertEqual(errors[1].subject, wf)
        self.assertIn("no execution layers", errors[1].local_error)

    def test_no_mco_parameters(self):
        wf = self.workflow
        wf.mco_model = self.plugin.mco_factories[0].create_model()

        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[0].subject, wf.mco_model)
        self.assertIn("no defined parameters", errors[0].local_error)

    def test_no_mco_kpis(self):
        wf = self.workflow
        mco_factory = self.plugin.mco_factories[0]
        wf.mco_model = mco_factory.create_model()

        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[0].subject, wf.mco_model)
        self.assertIn("no defined KPIs", errors[1].local_error)

    def test_empty_parameter_options(self):
        wf = self.workflow
        mco_factory = self.plugin.mco_factories[0]
        wf.mco_model = mco_factory.create_model()
        parameter_factory = mco_factory.parameter_factories[0]
        wf.mco_model.parameters.append(parameter_factory.create_model())

        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[1].subject, wf.mco_model.parameters[0])
        self.assertIn("MCO parameter is not named", errors[1].local_error)

    def test_empty_kpi_options(self):
        wf = self.workflow
        mco_factory = self.plugin.mco_factories[0]
        wf.mco_model = mco_factory.create_model()
        kpi = KPISpecification(name='')
        wf.mco_model.kpis.append(kpi)

        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[1].subject, wf.mco_model.kpis[0])
        self.assertIn("KPI is not named", errors[1].local_error)

    def test_empty_execution_layer(self):
        wf = self.workflow
        mco_factory = self.plugin.mco_factories[0]
        wf.mco_model = mco_factory.create_model()
        parameter_factory = mco_factory.parameter_factories[0]
        wf.mco_model.parameters.append(parameter_factory.create_model())
        wf.mco_model.parameters[0].name = "name"
        wf.mco_model.parameters[0].type = "Type"
        wf.mco_model.kpis.append(KPISpecification(name='name'))

        layer = ExecutionLayer()
        wf.execution_layers.append(layer)
        errors = verify_workflow(wf)

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].subject, wf.execution_layers[0])

    def test_data_sources(self):
        wf = self.workflow
        mco_factory = self.plugin.mco_factories[0]
        wf.mco_model = mco_factory.create_model()
        parameter_factory = mco_factory.parameter_factories[0]
        wf.mco_model.parameters.append(parameter_factory.create_model())
        wf.mco_model.parameters[0].name = "name"
        wf.mco_model.parameters[0].type = "Type"
        wf.mco_model.kpis.append(KPISpecification(name='name'))

        layer = ExecutionLayer()
        wf.execution_layers.append(layer)
        ds_factory = self.plugin.data_source_factories[0]
        ds_model = ds_factory.create_model()
        layer.data_sources.append(ds_model)

        errors = verify_workflow(wf)
        self.assertEqual(errors[0].subject, ds_model)
        self.assertIn("The number of input slots is incorrect.",
                      errors[0].local_error)

        ds_model.input_slot_info.append(
            InputSlotInfo(name="name")
        )

        errors = verify_workflow(wf)
        self.assertEqual(errors[0].subject, ds_model)
        self.assertIn("The number of output slots is incorrect.",
                      errors[0].local_error)

        ds_model.output_slot_info.append(
            OutputSlotInfo(name="name")
        )

        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 0)

        ds_model.input_slot_info[0].name = ''
        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 1)
        self.assertIn("Input slot is not named",
                      errors[0].local_error)

        ds_model.output_slot_info[0].name = ''
        errors = verify_workflow(wf)
        self.assertEqual(len(errors), 3)
        self.assertIn("All output variables have undefined names",
                      errors[1].local_error)
        self.assertIn("An output variable has an undefined name",
                      errors[2].local_error)
