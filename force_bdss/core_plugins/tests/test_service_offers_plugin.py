import unittest

from envisage.api import ServiceOffer

from force_bdss.tests.dummy_classes.extension_plugin import \
    DummyServiceOffersPlugin


class TestServiceOffersPlugin(unittest.TestCase):

    def setUp(self):

        self.plugin = DummyServiceOffersPlugin()

    def test_get_service_offer_factories(self):

        protocol_factories = self.plugin.get_service_offer_factories()
        self.assertEqual(1, len(protocol_factories))
        protocol, factories = protocol_factories[0]
        self.assertEqual(1, len(factories))

    def test_service_offers_default(self):

        self.assertEqual(
            1, len(self.plugin.service_offers)
        )
        self.assertIsInstance(
            self.plugin.service_offers[0], ServiceOffer
        )
