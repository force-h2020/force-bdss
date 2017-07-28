import unittest

from force_bdss.core_plugins.dummy.dummy_dakota.dakota_model import \
    DummyDakotaModel
from force_bdss.mco.base_mco_bundle import BaseMCOBundle
from force_bdss.mco.parameters.core_mco_parameters import RangedMCOParameter, \
    RangedMCOParameterFactory

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.core_plugins.dummy.dummy_dakota.dakota_optimizer import \
    DummyDakotaOptimizer


class TestDakotaOptimizer(unittest.TestCase):
    def setUp(self):
        self.bundle = mock.Mock(spec=BaseMCOBundle)
        self.bundle.plugin = mock.Mock()
        self.bundle.plugin.application = mock.Mock()
        self.bundle.plugin.application.workflow_filepath = "whatever"

    def test_initialization(self):
        opt = DummyDakotaOptimizer(self.bundle)
        self.assertEqual(opt.bundle, self.bundle)

    def test_run(self):
        opt = DummyDakotaOptimizer(self.bundle)
        model = DummyDakotaModel(self.bundle)
        model.parameters = [
            RangedMCOParameter(mock.Mock(spec=RangedMCOParameterFactory),
                lower_bound=1,
                upper_bound=3,
                initial_value=2)
        ]

        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(return_value=("1 2 3", ""))

        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = mock_process
            opt.run(model)

        self.assertEqual(mock_popen.call_count, 2)
