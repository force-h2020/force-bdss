Introduction
------------

The Business Decision System is the CLI support for the evaluation of
Pareto front computations. It is a single executable ``force_bdss`` that
interprets a workflow specification file, normally generated via the GUI
workflow manager.

By itself, the executable and the code implementing it provides no
functionality. All functionality comes from external plugins, extending the
API to provide new entities, specifically:

- Multi Criteria Optimizer (MCO)
- DataSources, which can be a simulator or just a database
- Key Performance Indicator (KPI) Calculators
- Notification Listeners, like a remote database which retrieve data during the
  computation

Plugin support requires compliancy to the Force BDSS api for plugins.
Extensions are registered via setuptools entry points.

Execution of the force bdss executable is simple. Invoke with::

    force_bdss workflow.json
