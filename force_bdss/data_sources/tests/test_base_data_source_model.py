import unittest

from force_bdss.core.input_slot_map import InputSlotMap

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.data_sources.base_data_source_bundle import \
    BaseDataSourceBundle
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel


class DummyDataSourceModel(BaseDataSourceModel):
    pass


class TestBaseDataSourceModel(unittest.TestCase):
    def test_getstate(self):
        model = DummyDataSourceModel(mock.Mock(spec=BaseDataSourceBundle))
        self.assertEqual(
            model.__getstate__(),
            {
                "__traits_version__": "4.6.0",
                "input_slot_maps": [],
                "output_slot_names": []
            })

        model.input_slot_maps = [
            InputSlotMap(
                name="foo"
            ),
            InputSlotMap(
                name="bar"
            )
        ]
        model.output_slot_names = ["baz", "quux"]

        self.assertEqual(
            model.__getstate__(),
            {
                "__traits_version__": "4.6.0",
                "input_slot_maps": [
                    {
                        "__traits_version__": "4.6.0",
                        "source": "Environment",
                        "name": "foo"
                    },
                    {
                        "__traits_version__": "4.6.0",
                        "source": "Environment",
                        "name": "bar"
                    }
                ],
                "output_slot_names": ["baz", "quux"]
            })
