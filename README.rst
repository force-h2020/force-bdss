FORCE BDSS
----------

.. image:: https://travis-ci.com/force-h2020/force-bdss.svg?branch=master
   :target: https://travis-ci.com/force-h2020/force-bdss
   :alt: Build status

.. image:: http://codecov.io/github/force-h2020/force-bdss/coverage.svg?branch=master
   :target: http://codecov.io/github/force-h2020/force-bdss?branch=master
   :alt: Coverage status

.. image:: https://readthedocs.org/projects/force-bdss/badge/?version=latest
    :target: https://force-bdss.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This repository contains the implementation of the Business Decision Support System (BDSS).
It is implemented under the Formulations and Computational Engineering (FORCE) project within Horizon 2020
(`NMBP-23-2016/721027 <https://www.the-force-project.eu>`_).

Installation
------------

To install, follow the `installation instructions <doc/source/installation.rst>`_

Developer Notes
---------------

Please also read the `documentation <doc/source/plugin_development.rst>`_ regarding plugin development for the BDSS,
as well as the `developer guidelines <doc/source/developer_guidelines.rst>`_ for contributing code
to FORCE projects in general.

Documentation
-------------

Full documentation is being hosted at the `BDSS ReadTheDocs page <https://force-bdss.readthedocs.io>`_.

Alternatively, to build the documentation locally in the ``doc/build`` directory, run::

    python -m ci docs
