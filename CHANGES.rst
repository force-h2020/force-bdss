FORCE BDSS Changelog
--------------------

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

Internal changes:

- Changed internal plugin ids to prevent conflicts with external ones (#131)

Release 0.2.0
-------------

- Development of infrastructure to support ITWM example code.

Release 0.1.0
-------------

- Initial release. Implements basic functionality of the BDSS and its
  plugin system.
