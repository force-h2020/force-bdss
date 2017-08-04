Plugin Development
------------------

A single Plugin can provide one or more of the pluggable entities
described elsewhere (MCO/KPICalculators/DataSources). Multiple plugins can
be installed to provide a broad range of functionalities.

Plugins must return Factories. Each Factory provides factory methods for 
one of the above pluggable entities and its associated classes.

To implement a new plugin, you must

- define the entity you want to extend (e.g. ``MyOwnDataSource``) as a derived
  class of the appropriate class (e.g. BaseDataSource), and reimplement
  the appropriate methods.
- Define the model that this DataSource needs, by extending
  ``BaseDataSourceModel`` and adding, with traits, the appropriate data that
  are required by your data source to perform its task.
- Define the Factory, by reimplementing BaseDataSourceFactory and reimplementing
  its ``create_*`` methods to return the above entities.
- Define a ``Plugin`` by reimplementing ``BaseExtensionPlugin`` and
  reimplementing its initialization defaults methods to return your factory.
- add the plugin class in the setup.py entry_point, under the namespace
  ``force.bdss.extensions``
