import os
from setuptools import setup, find_packages

VERSION = "0.1.0"


# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()


def write_version_py():
    filename = os.path.join(
        os.path.dirname(__file__),
        'force_bdss',
        'version.py')
    ver = "__version__ = '{}'\n"
    with open(filename, 'w') as fh:
        fh.write(ver.format(VERSION))


write_version_py()

setup(
    name="force_bdss",
    version=VERSION,
    entry_points={
        'console_scripts': [
            'force_bdss = force_bdss.cli.force_bdss:run',
        ],
        "force.bdss.extensions": [
            "dummy = force_bdss.core_plugins.dummy.dummy_plugin:DummyPlugin",
        ]
    },
    packages=find_packages(),
    install_requires=[
        "envisage >= 4.6.0",
        "click >= 6.7",
        "stevedore >= 1.24.0",
        "six >= 1.10.0",
    ]
)
