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
- Notification Listeners, like a remote database which retrieve data during the
  computation
- UI Hooks, which permit to define additional operations which will be executed
  at specific moments in the UI lifetime (before and after exectution of the
  bdss, before saving the workflow)

Plugin support requires compliancy to the Force BDSS api for plugins.
Extensions are registered via setuptools entry points.

Execution of the force bdss executable is simple. Invoke with::

    force_bdss workflow.json
