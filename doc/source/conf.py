# -*- coding: utf-8 -*-

#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import sphinx.environment
from docutils.utils import get_source_line
import sys
import os


sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..")
    )

from force_bdss.version import __version__ as RELEASE

MOCK_MODULES=[]

def _warn_node(self, msg, node, **kwargs):
    if not msg.startswith('nonlocal image URI found:'):
        self._warnfunc(msg, '%s:%s' % get_source_line(node), **kwargs)

sphinx.environment.BuildEnvironment.warn_node = _warn_node

def mock_modules():
    import sys

    from unittest.mock import MagicMock

    class Mock(MagicMock):
        @classmethod
        def __getattr__(cls, name):
            return Mock()

        def __call__(self, *args, **kwards):
            return Mock()

    sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)
    print('mocking {}'.format(MOCK_MODULES))

mock_modules()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'FORCE'
copyright = u'2017, FORCE Project'
version = ".".join(RELEASE.split(".")[0:3])
release = RELEASE
pygments_style = 'sphinx'
html_theme = 'classic'
html_theme_options = {'body_max_width': '80%'}
html_static_path = ['_static']
html_logo = '_static/force_logo.png'
htmlhelp_basename = 'FORCEdoc'
intersphinx_mapping = {'http://docs.python.org/': None}
apidoc_module_dir = '../../force_bdss'
apidoc_output_dir = 'api'
apidoc_excluded_paths = ['*tests*', 'api.py']
apidoc_separate_modules = False
