from setuptools import setup, find_packages

VERSION = "0.1.0.dev0"

setup(
    name="force_bdss",
    version=VERSION,
    entry_points={
        'console_scripts': [
            'force_bdss = force_bdss.cli.force_bdss:run',
        ],
        "force.bdss.extensions": [
            "mco = force_bdss.core_plugins.test_mco."
            "multi_criteria_optimizers_plugin:MultiCriteriaOptimizersPlugin",
            "data_source = force_bdss.core_plugins.test_data_sources."
            "data_sources_plugin:DataSourcesPlugin",
        ]
    },
    packages=find_packages(),
    install_requires=[
        "envisage >= 4.6.0",
        "click >= 6.7",
        "stevedore >= 1.24.0",
        "six >= 1.10.0"
    ]
)
