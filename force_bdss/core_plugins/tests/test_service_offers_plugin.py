import sys

from unittest import TestCase, mock

from envisage.api import ServiceOffer

from force_bdss.tests.dummy_classes.extension_plugin import \
    DummyServiceOffersPlugin


MOCK_IMPORT = 'builtins.__import__'

class TestServiceOffersPlugin(TestCase):

    def setUp(self):

        self.plugin = DummyServiceOffersPlugin()

    def test___init__(self):
        """Tests instantiation of <class ServiceOffersPlugin>
        .service_offers only occurs after attribute is called"""
        with mock.patch(MOCK_IMPORT) as mock_import, \
             mock.patch.object(DummyServiceOffersPlugin,
                   'get_service_offer_factories') as mock_default:
            plugin = DummyServiceOffersPlugin()
            mock_default.assert_not_called()
            mock_import.assert_not_called()

            self.assertIsNotNone(plugin.service_offers)
            mock_default.assert_called()
            mock_import.called_once()

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
