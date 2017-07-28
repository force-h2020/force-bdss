from setuptools import setup, find_packages

VERSION = "0.1.0.dev2"

def write_version_py():
    with open("force_bdss/__version__.py", "w") as f:
        f.write("VERSION = '{}'".format(VERSION))

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
        "numpy >= 1.12.0",
    ]
)
