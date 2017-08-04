import unittest

from force_bdss.core_plugins.dummy.dummy_dakota.parameters import (
    RangedMCOParameter,
    RangedMCOParameterFactory
)
from force_bdss.core_plugins.dummy.dummy_dakota.dakota_model import (
    DummyDakotaModel
)
from force_bdss.mco.base_mco_factory import BaseMCOFactory

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.core_plugins.dummy.dummy_dakota.dakota_optimizer import \
    DummyDakotaOptimizer


class TestDakotaOptimizer(unittest.TestCase):
    def setUp(self):
        self.factory = mock.Mock(spec=BaseMCOFactory)
        self.factory.plugin = mock.Mock()
        self.factory.plugin.application = mock.Mock()
        self.factory.plugin.application.workflow_filepath = "whatever"

    def test_initialization(self):
        opt = DummyDakotaOptimizer(self.factory)
        self.assertEqual(opt.factory, self.factory)

    def test_run(self):
        opt = DummyDakotaOptimizer(self.factory)
        model = DummyDakotaModel(self.factory)
        model.parameters = [
            RangedMCOParameter(
                mock.Mock(spec=RangedMCOParameterFactory),
                lower_bound=1,
                upper_bound=3,
                initial_value=2)
        ]

        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(return_value=(b"1 2 3", b""))

        with mock.patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = mock_process
            opt.run(model)

        self.assertEqual(mock_popen.call_count, 2)
