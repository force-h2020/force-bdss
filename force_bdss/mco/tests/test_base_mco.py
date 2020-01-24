import testfixtures
import unittest
import warnings

from force_bdss.mco.base_mco import NotifyEventWarning
from force_bdss.mco.i_mco_factory import IMCOFactory
from force_bdss.tests.dummy_classes.mco import DummyMCO

from unittest import mock


class TestNotifyEventWarning(unittest.TestCase):
    """NOTE: this class should be removed alongside BaseMCO.event"""
    def test_warn(self):

        expected_message = (
            "Use of the BaseMCO.event attribute is now deprecated and will"
            " be removed in version 0.5.0. Please replace any uses of the "
            "BaseMCO.notify and BaseMCO.notify_new_point method with the "
            "equivalent BaseMCOModel.notify and "
            "BaseMCOModel.notify_new_point methods respectively")

        expected_log = (
            "force_bdss.mco.base_mco",
            "WARNING",
            expected_message,
        )

        with testfixtures.LogCapture() as capture, \
                warnings.catch_warnings(record=True) as errors:

            NotifyEventWarning.warn()

            capture.check(expected_log)
            self.assertEqual(expected_message, str(errors[0].message))


class TestBaseMultiCriteriaOptimizer(unittest.TestCase):
    def test_initialization(self):
        factory = mock.Mock(spec=IMCOFactory)
        mco = DummyMCO(factory)

        self.assertEqual(mco.factory, factory)
