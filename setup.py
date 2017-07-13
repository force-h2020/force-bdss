from setuptools import setup

VERSION = "0.1.0.dev0"

setup(
    name="force_bdss",
    version=VERSION,
    entry_points={
        'console_scripts': [
            'force_bdss = force_bdss.cli.force_bdss:run',
        ]},
    install_requires=[
        "envisage >= 4.6.0",
        "click >= 6.7"
    ]
)
