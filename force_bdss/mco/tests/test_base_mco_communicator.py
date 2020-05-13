#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from force_bdss.mco.i_mco_factory import IMCOFactory
from force_bdss.tests.dummy_classes.mco import DummyMCOCommunicator

from unittest import mock


class TestBaseMCOCommunicator(unittest.TestCase):
    def test_initialization(self):
        factory = mock.Mock(spec=IMCOFactory)
        mcocomm = DummyMCOCommunicator(factory)

        self.assertEqual(mcocomm.factory, factory)
