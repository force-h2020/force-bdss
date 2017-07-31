import unittest

from force_bdss.base_extension_plugin import (
    BaseExtensionPlugin)
from force_bdss.ids import bundle_id, mco_parameter_id
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.application import Application

from force_bdss.bundle_registry_plugin import BundleRegistryPlugin
from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle
from force_bdss.kpi.i_kpi_calculator_bundle import IKPICalculatorBundle
from force_bdss.mco.i_mco_bundle import \
    IMCOBundle


class TestBundleRegistry(unittest.TestCase):
    def setUp(self):
        self.plugin = BundleRegistryPlugin()
        self.app = Application([self.plugin])
        self.app.start()
        self.app.stop()

    def test_initialization(self):
        self.assertEqual(self.plugin.mco_bundles, [])
        self.assertEqual(self.plugin.data_source_bundles, [])
        self.assertEqual(self.plugin.kpi_calculator_bundles, [])


class MySuperPlugin(BaseExtensionPlugin):
    def _mco_bundles_default(self):
        return [
            mock.Mock(
                spec=IMCOBundle,
                id=bundle_id("enthought", "mco1"),
                parameter_factories=mock.Mock(return_value=[
                    mock.Mock(
                        spec=BaseMCOParameterFactory,
                        id=mco_parameter_id("enthought", "mco1", "ranged")
                    )
                ]),
            )]

    def _data_source_bundles_default(self):
        return [mock.Mock(spec=IDataSourceBundle,
                          id=bundle_id("enthought", "ds1")),
                mock.Mock(spec=IDataSourceBundle,
                          id=bundle_id("enthought", "ds2"))]

    def _kpi_calculator_bundles_default(self):
        return [mock.Mock(spec=IKPICalculatorBundle,
                          id=bundle_id("enthought", "kpi1")),
                mock.Mock(spec=IKPICalculatorBundle,
                          id=bundle_id("enthought", "kpi2")),
                mock.Mock(spec=IKPICalculatorBundle,
                          id=bundle_id("enthought", "kpi3"))]


class TestBundleRegistryWithContent(unittest.TestCase):
    def setUp(self):
        self.plugin = BundleRegistryPlugin()
        self.app = Application([self.plugin, MySuperPlugin()])
        self.app.start()
        self.app.stop()

    def test_initialization(self):
        self.assertEqual(len(self.plugin.mco_bundles), 1)
        self.assertEqual(len(self.plugin.data_source_bundles), 2)
        self.assertEqual(len(self.plugin.kpi_calculator_bundles), 3)

    def test_lookup(self):
        mco_id = bundle_id("enthought", "mco1")
        parameter_id = mco_parameter_id("enthought", "mco1", "ranged")
        self.assertEqual(self.plugin.mco_bundle_by_id(mco_id).id, mco_id)
        self.plugin.mco_parameter_factory_by_id(mco_id, parameter_id)

        for entry in ["ds1", "ds2"]:
            id = bundle_id("enthought", entry)
            self.assertEqual(self.plugin.data_source_bundle_by_id(id).id, id)

        for entry in ["kpi1", "kpi2", "kpi3"]:
            id = bundle_id("enthought", entry)
            self.assertEqual(self.plugin.kpi_calculator_bundle_by_id(id).id,
                             id)


if __name__ == '__main__':
    unittest.main()
