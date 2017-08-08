Plugin Development
------------------

A single Plugin can provide one or more of the pluggable entities
described elsewhere (MCO/KPICalculators/DataSources). Multiple plugins can
be installed to provide a broad range of functionalities.

Plugins must return Factories. Each Factory provides factory methods for 
one of the above pluggable entities and its associated classes.

To implement a new plugin, you must

- define the entity you want to extend (e.g. ``MyOwnDataSource``) as a derived
  class of the appropriate class (e.g. ``BaseDataSource``), and reimplement
  the appropriate methods:
  - ``run()``: where the actual computation takes place, given the
    configuration options specified in the model (which is received as an
    argument). It is strongly advised that the ``run()`` method is stateless.
  - ``slots()``: must return a 2-tuple of tuples. Each tuple contains instances
    of the ``Slot`` class. Slots are the input and output entities of the
    data source or KPI calculator. Given that this information depends on the
    configuration options, ``slots()`` accepts the model and must return the
    appropriate values according to the model options.
- Define the model that this ``DataSource`` needs, by extending
  ``BaseDataSourceModel`` and adding, with traits, the appropriate data that
  are required by your data source to perform its task.
  If a trait change in your model influences the input/output slots, you must
  make sure that the event ``changes_slots`` is fired as a consequence of
  those changes. This will notify the UI that the new slots need to be
  recomputed and presented to the user. Failing to do so will have unexpected
  consequences.
- Define the Factory, by reimplementing BaseDataSourceFactory and reimplementing
  its ``create_*`` methods to return the above entities.
- Define a ``Plugin`` by reimplementing ``BaseExtensionPlugin`` and
  reimplementing its initialization defaults methods to return your factory.
- add the plugin class in the setup.py entry_point, under the namespace
  ``force.bdss.extensions``


