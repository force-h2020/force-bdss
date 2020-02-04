from tempfile import NamedTemporaryFile
from unittest import TestCase, mock

from force_bdss.io.file_tree_builder import (
    FileTreeBuilder
)

FILE_TREE_MKPATH = (
    "force_bdss.io.file_tree_builder.os.mkdir"
)


def mock_empty(value):
    return None


class TestFileTreeBuilder(TestCase):

    def setUp(self):

        self.builder = FileTreeBuilder(
            root='test_experiment_1'
        )

    def test_add_path(self):

        self.assertDictEqual({}, self.builder._file_tree)
        self.builder.add_path("test_experiment_1/new_folder")

        self.assertDictEqual(
            {
                'test_experiment_1': {
                    'new_folder': {}
                }
            },
            self.builder._file_tree
        )

        # Test name nested folder name redundancy
        self.builder.add_path(
            "test_experiment_1/another_folder/nested_1/nested_1")

        self.assertDictEqual(
            {
                'test_experiment_1': {
                    'new_folder': {},
                    'another_folder': {
                        'nested_1': {
                            'nested_1': {}
                        }
                    }
                }
            },
            self.builder._file_tree
        )

    def test_add_folders(self):

        self.builder.add_folders(
            "test_experiment_1/new_folder", ["folder 1", "folder 2"]
        )

        self.assertDictEqual(
            {
                'test_experiment_1': {
                    'new_folder': {
                        "folder 1": {},
                        "folder 2": {}
                    }
                }
            },
            self.builder._file_tree
        )

        # Test previously created folders are not overwritten
        self.builder.add_path(
            "test_experiment_1/new_folder/folder 2/new_folder")
        self.builder.add_folders(
            "test_experiment_1/new_folder",
            ["folder 2", "folder 3"]
        )
        self.assertDictEqual(
            {
                'test_experiment_1': {
                    'new_folder': {
                        "folder 1": {},
                        "folder 2": {
                            "new_folder": {}
                        },
                        "folder 3": {}
                    }
                }
            },
            self.builder._file_tree
        )

    def test__make_directory(self):

        with mock.patch(FILE_TREE_MKPATH) as mock_mkdir:
            with NamedTemporaryFile() as tmp_file:
                self.builder._make_directory(tmp_file.name)
            mock_mkdir.assert_not_called()

        with mock.patch(FILE_TREE_MKPATH) as mock_mkdir:
            mock_mkdir.side_effect = mock_empty
            self.builder._make_directory('')
            mock_mkdir.assert_called()

    def test__create_directory_list(self):
        self.builder._file_tree = {
            '1_build': {},
            '2_minimize': {},
            '3_production': {}
        }
        directory_list = self.builder._create_directory_list()
        print(directory_list)
        self.assertListEqual(
            ['test_experiment_1',
             'test_experiment_1/1_build',
             'test_experiment_1/2_minimize',
             'test_experiment_1/3_production'],
            directory_list
        )

        self.builder._file_tree['1_build']['1_nested_folder'] = {}

        directory_list = self.builder._create_directory_list()
        self.assertListEqual(
            ['test_experiment_1',
             'test_experiment_1/1_build',
             'test_experiment_1/1_build/1_nested_folder',
             'test_experiment_1/2_minimize',
             'test_experiment_1/3_production'],
            directory_list
        )

    def test_build_file_tree(self):
        self.builder._file_tree = {
            '1_build': {},
            '2_minimize': {},
            '3_production': {},
        }
        with mock.patch(FILE_TREE_MKPATH) as mock_mkdir:
            mock_mkdir.side_effect = mock_empty
            self.builder.build_file_tree()
            self.assertEqual(4, mock_mkdir.call_count)
