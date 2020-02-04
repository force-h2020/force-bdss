import logging
import os
import collections

from traits.api import HasStrictTraits, Dict, Directory

from force_bdss.utilities import path_generator

log = logging.getLogger(__name__)


class FileTreeBuilder(HasStrictTraits):
    """Class builds nested file trees"""

    #: Location to create file tree in. (By default, the
    #: current working directory)
    root = Directory()

    # --------------------
    #  Private Attributes
    # --------------------

    #: Ordered dictionary to hold nested directories
    _file_tree = Dict(Directory, Dict)

    def __file_tree_default(self):
        return collections.OrderedDict()

    # --------------------
    #   Private Methods
    # --------------------

    def _make_directory(self, directory):
        """Creates new directory if path does not already exist"""
        if not os.path.exists(directory):
            os.mkdir(directory)

    def _create_directory_list(self):
        """Iterate through each branch in file tree and
        return each directory that needs to be created in
        an appropriate order."""
        directory_list = [self.root]
        directory_list += [
            path for path in path_generator(
                self._file_tree, self.root)
        ]
        return directory_list
    # --------------------
    #    Public Methods
    # --------------------

    def add_path(self, path):
        """Iteratively add a single path to file tree. Do not
        edit an existing paths"""

        directories = path.split('/')
        directory = self._file_tree

        for folder in directories:
            if folder not in directory:
                directory[folder] = {}
            directory = directory[folder]

        return directory

    def add_folders(self, path, folders):
        """Add a directory with a list of folders to the
        file tree. Do not edit an existing folder"""

        directory = self.add_path(path)

        for folder in folders:
            if folder not in directory:
                directory[folder] = {}

    def build_file_tree(self):
        """Builds the file tree"""
        directory_list = self._create_directory_list()
        for directory in directory_list:
            self._make_directory(directory)
