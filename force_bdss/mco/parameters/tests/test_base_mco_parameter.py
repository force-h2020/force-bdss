import unittest

from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter


class DummyParameter(BaseMCOParameter):
    pass


class TestBaseMCOParameter(unittest.TestCase):
    def test_instantiation(self):
        factory = mock.Mock(spec=BaseMCOParameterFactory)
        param = DummyParameter(factory)
        self.assertEqual(param.factory, factory)
