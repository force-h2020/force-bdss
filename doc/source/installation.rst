Installation
============

The BDSS, the Workflow Manager and all plugins can be cloned from the
`Force 2020 github respositories <https://github.com/force-h2020>`_.
For the BDSS and Workflow Manager,

.. code-block:: console

    git clone https://github.com/force-h2020/force-bdss
    git clone https://github.com/force-h2020/force-wfmanager


Enthought Deployment Manager
----------------------------

The BDSS, the Workflow Manager and plugins must be installed through the `Enthought Deployment
Manager (EDM) <https://www.enthought.com/enthought-deployment-manager/>`_, a python
virtual environment and package manager. For new users it is worth examining EDM's
`documentation <http://docs.enthought.com/edm/>`_.

To install EDM, follow the instructions specific to your operating system
`,here <https://docs.enthought.com/edm/installation.html>`_.


The Bootstrap Environment
-------------------------

Once EDM is installed create a 'bootstrap' environment from which you can install
the BDSS, Workflow Manager and plugins,

.. code-block:: console

    edm install -e bootstrap -y click setuptools

Note that 'bootstrap' can be replaced by any name to the same effect. Now you can enter
``bootstrap`` with,

.. code-block:: console

    edm shell -e bootstrap

and your shell prompt is prefixed with ``(bootstrap)``.


The BDSS Runtime Environment
----------------------------

Although repositories (BDSS, etc) are installed *from* the ``bootstrap`` environment, they are
installed *into* a separate environment, within which the BDSS and the Workflow Manager will
actually run. Thus this environment has also to be created before installation. To do this
first cd into the cloned force-bdss respository,

.. code-block:: console

    ~/Force-Project (bootstrap)$ cd force-bdss

and then,

.. code-block:: console

    ~/Force-Project/force-bdss (bootstrap)$ python -m ci build-env

This creates a environment called ``force-pyXX``, where ``XX`` refers to the python version that
the environment runs (e.g. ``force-py36`` for python 3.6) . You will now see it in the list of EDM environments,

.. code-block:: console

    (bootstrap)$ edm environments list

    >> * bootstrap     cpython  3.6.9+2  win_x86_64  msvc2015  ~\.edm\envs\bootstrap
    >>   force-py36    cpython  3.6.9+2  win_x86_64  msvc2015  ~.edm\envs\force-pyXX


Repository Installation
-----------------------

From the ``bootstrap`` environment (not ``force-pyXX``!), for each respository in turn,
cd into its directory and then install it with ``python -m ci install``. i.e.,

.. code-block:: console

    ~/Force-Project/force-bdss (bootstrap)$ python -m ci install

    ~/Force-Project/force-bdss (bootstrap)$ cd ../force-wfmanager
    ~/Force-Project/force-wfmanager (bootstrap)$ python -m ci install

    ...etc
