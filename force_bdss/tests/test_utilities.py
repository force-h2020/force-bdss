import unittest

from force_bdss.utilities import (
    pop_dunder_recursive,
    pop_recursive,
    path_generator
)


class TestDictUtils(unittest.TestCase):

    def test_path_generator(self):

        nested_dict = {
            'first': {
                'second_1': {
                    'third': {}
                },
                'second_2': {
                    'third': {},
                    'not_a_dict': []
                }
            }
        }

        paths = [
            key for key in path_generator(nested_dict)
        ]

        self.assertListEqual(
            ['first', 'first/second_1', 'first/second_1/third',
             'first/second_2', 'first/second_2/third'],
            paths
        )

        paths = [
            key for key in path_generator(nested_dict, 'root')
        ]

        self.assertListEqual(
            ['root/first', 'root/first/second_1',
             'root/first/second_1/third',
             'root/first/second_2', 'root/first/second_2/third'],
            paths
        )

    def test_dunder_recursive(self):
        test_dict = {
            "__traits_version__": "4.6.0",
            "some_important_data": {
                "__traits_version__": "4.6.0",
                "value": 10,
            },
            "_some_private_data": {"__instance_traits__": ["yes", "some"]},
            "___": {"__": "a", "foo": "bar"},
            "list_of_dicts": [
                {"__bad_key__": "bad", "good_key": "good"},
                {"also_good_key": "good"},
            ],
        }
        expected = {
            "some_important_data": {"value": 10},
            "_some_private_data": {},
            "list_of_dicts": [{"good_key": "good"}, {"also_good_key": "good"}],
        }
        self.assertEqual(pop_dunder_recursive(test_dict), expected)

    def test_pop_recursive(self):
        test_dictionary = {
            "K1": {"K1": "V1", "K2": "V2", "K3": "V3"},
            "K2": ["V1", "V2", {"K1": "V1", "K2": "V2", "K3": "V3"}],
            "K3": "V3",
            "K4": ("V1", {"K3": "V3"}),
        }

        result_dictionary = {
            "K1": {"K1": "V1", "K2": "V2"},
            "K2": ["V1", "V2", {"K1": "V1", "K2": "V2"}],
            "K4": ("V1", {}),
        }

        test_result_dictionary = pop_recursive(test_dictionary, "K3")
        self.assertEqual(test_result_dictionary, result_dictionary)

        small_dict = {"key": "value"}
        missing_key = "another_key"
        self.assertDictEqual(
            pop_recursive(small_dict, missing_key), small_dict
        )
