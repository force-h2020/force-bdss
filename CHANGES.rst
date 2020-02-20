FORCE BDSS Changelog
====================

Release 0.4.0
-------------

Released:

Release notes
~~~~~~~~~~~~~

Version 0.4.0 is a major update to the BDSS package, and includes a number of
backward incompatible changes, including:

* Major refactoring of ``BDSSApplication`` class to separate dependency on Envisage library
    -  Removed classes: ``BaseCoreDriver``, ``CoreEvaluationDriver``, ``CoreMCODriver``
    -  New classes: ``WorkflowFile``
    - ``BaseFactory`` class no longer carries around the Envisage plugin that it is
      instantiated from, only a reference to the name and id
    - Communication pathway for ``BaseDriverEvents`` during an MCO run has been changed,
      rendering some methods obsolete
* New workflow file formatting version 1.1

The following people contributed
code changes for this release:

* Corran Webster
* James Johnson
* Frank Longford
* Nicola De Mitri
* Petr Kungurtsev

Features
~~~~~~~~

* New ``ServiceOfferExtensionPlugin`` class (#227, #228), providing support for developers
  to contribute custom UI objects for the WfManager in a BDSS plugin.
* New ``WorkflowFile`` class (#220) containing all functionalities required to describe, read and write
  ``Workflow`` objects
* Selection of useful objects from plugins have been incorporated into core library
    - ``BaseMCOParameter`` subclasses (#242, #253, #255)
    - ``BaseCSVWriter*`` classes (#244), subclasses of ``BaseNotificationListener``
* New ``BaseOptimizerEngine`` class (#243), providing a standard interface between black-box
  optimization libraries (scipy, acado, nevergrad etc.) and functionalities of the ``BaseMCO`` class
* ``WeightedOptimizer`` subclass (#243) ported from ITWM plugin and included as part of core library
* ``BaseDriverEvents`` class now includes serialization and deserilaization methods (#247, #248, #275),
  generally based on those ported from the WfManager
* New ``WeightedMCOStartEvent`` and ``WeightedMCOProgressEvent`` (#274) included as part of core library,
  designed to be used alongside ``WeightedOptmizer``
* New ``UIEventNotificationMixin`` class (#296) and ability to stop and pause the ``OptimizeOperation``
  during an MCO run via a ``BaseDriverEvent``


Changes
~~~~~~~~

* Major refactoring of ``BDSSApplication`` (#220) to separate core features from Envisage
* ``BaseDriverEvents`` are propagated through the ``Workflow`` class, rather than the
  ``BaseMCO`` class (#269, #279).
* Replaced (now obsolete) ``Unicode`` traits in favour of ``Str`` (#265, #280)
* ``Workflow.mco`` attribute renamed to ``Workflow.mco_model`` (#257)
* ``WorkflowReader`` and ``WorkflowWriter`` classes refactored (#266, #263), resulting in new
  version 1.1 of workflow file formats

Fixes
~~~~~

* Fixes bug whereby ``WorkflowReader`` class could mutate workflow file (#
* Adds missing verification step for ``BaseMCOModel`` (#226) that requires at least 1 KPI
* Use ``tempfile`` library for creating temporary files (#273) in unit testing
* Fixes applied to remove weak design choice (#232, #276) of lower level objects accessing higher
  application-level objects
* API module improved to provide more classes (#277) to be accessible by external packages

Deprecations
~~~~~~~~~~~~

* ``BaseMCO.notify_driver_event`` method deprecated (#276), in favour of ``BaseMCOModel.notify_driver_event``
* ``BaseFactory`` class no longer carries around the Envisage plugin (#232) that it is
  instantiated from, only a reference to the name and id

Documentation
~~~~~~~~~~~~~

* Added documentation for contributing UI objects via ``ServiceOfferExtensionPlugin`` (#225, #228)
* Updated README (#262) including build status and links to installation instructions
* New auto-generated Sphinx documentation (#245, #251)

Maintenance and code organization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Envisage version updated to 4.9.2-2 (#222, #272, #289)
* Click version updated to 7.0-1 (#222)
* Flake version updated to 3.7.7-1 (#222)
* Sphinx version updated to 1.8.5-6 (#289)
* Stevedore version updated to 1.32-0 (#222, #289)
* EDM version updated to 2.1.0 in Travis CI (#223, #256) using python 3.6 bootstrap environment
* Travis CI now runs 2 jobs: Linux Ubuntu Bionic (#256) and MacOS (#223)
* Better handling of ClickExceptions in CI (#245)


Release 0.3.0
-------------

Backward incompatible changes that require rework of the plugins:

- Parameter factories are now instantiated once and for all (#135).
  - requires to change the plugins to return a list of factory classes
    in the get_parameter_factory_classes() method, instead of the
    parameter_factories() method. This method becomes a trait now.
    All plugins exporting an MCO must be updated.
- Design change of the notification infrastructure in MCO (#187):
    - the started and finished events do not need to be triggered anymore.
    - the new_data method is now obsolete and must be removed.
    - the notify_new_point() method must be called to inform of a new optimal
      point found. The routine accepts list of DataValue objects, not plain
      floats as before. The weights must also be passed.
    - A more generic notify() method is available to send arbitrary events
      (currently only MCOProgressEvent)

- Installation now requires two separate steps to build the environment
  and to install the BDSS (#180)
- Removed support for python2 (#179)
- Python version changed from 3.5 to 3.6, plus dependencies upgraded where
  possible (#198)

Internal changes:

- Changed internal plugin ids to prevent conflicts with external ones (#131)
- Fixed a bug where KPIs were assigned by the order they were returned,
  rather than their names (#204)
- Set the ETS toolkit to null for the command line app, this was causing
  slowdown by instantiating a Qt application which was never actually used
  (#206)

Release 0.2.0
-------------

- Development of infrastructure to support ITWM example code.

Release 0.1.0
-------------

- Initial release. Implements basic functionality of the BDSS and its
  plugin system.
