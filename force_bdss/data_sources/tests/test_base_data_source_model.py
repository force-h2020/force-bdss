import unittest

from force_bdss.core.input_slot_map import InputSlotInfo
from force_bdss.core.output_slot_info import OutputSlotInfo

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.data_sources.base_data_source_factory import \
    BaseDataSourceFactory
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel


class DummyDataSourceModel(BaseDataSourceModel):
    pass


class TestBaseDataSourceModel(unittest.TestCase):
    def test_getstate(self):
        model = DummyDataSourceModel(mock.Mock(spec=BaseDataSourceFactory))
        self.assertEqual(
            model.__getstate__(),
            {
                "__traits_version__": "4.6.0",
                "input_slot_info": [],
                "output_slot_info": []
            })

        model.input_slot_info = [
            InputSlotInfo(
                name="foo"
            ),
            InputSlotInfo(
                name="bar"
            )
        ]
        model.output_slot_info = [
            OutputSlotInfo(name="baz"),
            OutputSlotInfo(name="quux")
        ]

        self.assertEqual(
            model.__getstate__(),
            {
                "__traits_version__": "4.6.0",
                "input_slot_info": [
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
                "output_slot_info": [
                    {
                        "__traits_version__": "4.6.0",
                        "name": "baz",
                        "kpi": False
                    },
                    {
                        "__traits_version__": "4.6.0",
                        "name": "quux",
                        "kpi": False
                    }
                ]
            })
