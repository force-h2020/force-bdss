Plugin Development
------------------

Force BDSS is extensible through plugins. A plugin can be (and generally is)
provided as a separate python package that makes available some new classes.
Force BDSS will find these classes from the plugin at startup.

A single Plugin can provide one or more of the following entities:
``MCO``, ``DataSources``, ``NotificationListeners``, ``UIHooks``. It can optionally
provide ``DataViews`` to be used by the ``force_wfmanager`` GUI.

An example plugin implementation is available at:

https://github.com/force-h2020/force-bdss-plugin-enthought-example

To implement a new plugin, you must define at least four classes:

- The ``Plugin`` class itself.
- One of the entities you want to implement: a ``DataSource``,
  ``NotificationListener``, ``MCO``, or ``UIHook``.
- A ``Factory`` class for the entity above: it is responsible for creating the
  specific entity, for example, a ``DataSource``
- A ``Model`` class which contains configuration options for the entity.
  For example, it can contain login and password information so that its data
  source knows how to connect to a service. The ``Model`` is also shown visually
  in the ``force_wfmanager`` UI, so some visual aspects need to be configured as
  well.

The plugin is made available by having it defined in the ``setup.py`` file
``entry_points`` section, under the namespace ``force.bdss.extensions``. For example::

    entry_points={
        "force.bdss.extensions": [
            "enthought_example = "
            "enthought_example.example_plugin:ExamplePlugin",
        ]
    }


The plugin
^^^^^^^^^^

The plugin class must be

- Inheriting from ``force_bdss.api.BaseExtensionPlugin``
- Implement a ``id`` class member, that must be set to the result of
  calling the function ``plugin_id()``. For example::

    id = plugin_id("enthought", "example", 0)

- Implement a method ``get_factory_classes()`` returning a list of all
  the classes (NOT the instances) of the entities you want to export.
- Implement the methods ``get_name()``, ``get_version()`` and
  ``get_description()`` to return appropriate values. The ``get_version()``
  method in particular should return the same value as in the id (in this case
  zero). It is advised to extract this value in a global, module level
  constant.

The Factory
^^^^^^^^^^^

The factory must inherit from the appropriate factory for the given type.
For example, to create a DataSource, the factory must inherit from
``BaseDataSourceFactory``. It then needs these methods to be redefined

- ``get_identifier()``: must returns a unique string, e.g. a uuid or a
  memorable string that must be unique across your plugins, present and future.
- ``get_name()``: a memorable, user presentable name for the data source.
- ``get_description()``: a user presentable description.
- ``get_model_class()``: Must return the Model class.
- ``get_data_source_class()``: Must return the data source class.


The Model class
^^^^^^^^^^^^^^^

The model class must inherit from the appropriate Base model class, depending
on the entity, for example ``BaseDataSourceModel`` in case of a data source.

This class then must be treated as a Traits class, where you can use traits
to define the type of data it holds. Pay particular attention to those data
that can modify the slots. For those, add a ``changes_slots=True`` metadata
tag to the trait. This will notify the UI that the new slots need to be
recomputed and presented to the user. Failing to do so will have unexpected
consequences. Example::

    class MyModel(BaseDataSourceModel):
        normal_option = String()
        option_changing_slots = String(changes_slots=True)

Typically, options that change slots are those options that modify the behavior
of the computational engine, thus requiring more or less input (input slots)
or producing more or less output (output slots).

Many ``BaseModel`` subclasses also include a ``verify`` method, which is
called before an MCO run starts to ensure that the execution will be successful.
This verification step can also be triggered in the WfManager UI even before an MCO run is
submitted. For ``BaseDataSourceModel`` subclasses it is automatically performed whenever the
slots objects are updated, however developers can also include the ``verify=True`` metadata
on any additional trait that requires verification. Including this in example above::

    class MyModel(BaseDataSourceModel):
        normal_option = String(verify=True)
        option_changing_slots = String(changes_slots=True)

You can also define a UI view with traitsui (``import traitsui.api``). This is
recommended as the default view arranges the options in random order. To do
so, have a ``default_traits_view()`` method::

    def default_traits_view():
        return View(
            Item("normal_option"),
            Item("option_changing_slots")
        )

The DataSource class
^^^^^^^^^^^^^^^^^^^^

This is the "business end" of the data source, and where things are done.
The class must be derived from ``BaseDataSource``), and reimplement
the appropriate methods:

- ``run()``: where the actual computation takes place, given the
  configuration options specified in the model (which is received as an
  argument). It is strongly advised that the ``run()`` method is stateless.
- ``slots()``: must return a 2-tuple of tuples. Each tuple contains instances
  of the ``Slot`` class. Slots are the input and output entities of the
  data source. Given that this information depends on the
  configuration options, ``slots()`` accepts the model and must return the
  appropriate values according to the model options.

The MCO class
^^^^^^^^^^^^^

Like the data source, the MCO needs a model (derived from ``BaseMCOModel``),
a factory (derived from ``BaseMCOFactory``) and a MCO class (derived from
``BaseMCO``). Additional entities must be also provided:

- ``MCOCommunicator``: this class is responsible for handling communication
  between the MCO and the spawned process when the MCO is using a "subprocess"
  model, that is, the MCO invokes the force_bdss in evaluation mode to compute
  a single point.
- ``parameters``: We assume that different MCOs can support different parameter
  types for the generated variables. Currently, only the "range" type is
  commonly handled.


The factory then must be added to the plugin ``get_factory_classes()`` list.

The factory must define the following methods::

    def get_identifier(self):
    def get_name(self):
    def get_description(self):
    def get_model_class(self):

as in data source factory. The following::

    def get_optimizer_class(self):
    def get_communicator_class(self):

Must return classes of the MCO and the MCOCommunicator. Finally::

    def get_parameter_factory_classes(self):

Must return a list of classes of the parameter factories.

Optimizer Engines
~~~~~~~~~~~~~~~~~

The ``force_bdss.api`` package offers the ``BaseOptimizerEngine`` and
``SpaceSampler`` abstract classes, both of which are designed as utility objects for backend developers.

The ``BaseOptimizerEngine`` class provides a schema that can easily be reimplemented to
act as an interface between the BDSS and an external optimization library. Although it is not strictly
required to run an MCO, it is expected that a developer would import the object into a ``BaseMCO.run``
implementation, whilst providing any relevant pre and post processing of information for the specific used
case that the MCO is solving. The base class must simply define the following method::

    def optimize(self):

Which is expected to act as a generator, yielding values corresponding to optimised input parameters
and their corresponding KPIs. A concrete implementation of this base class, the ``WeightedOptimizerEngine``,
is provided that uses the ``SciPy`` library as a backend.

The ``SpaceSampler`` abstract class also acts as a utility class in order to sample
vectors of values from a given distribution. Implementations of this class could be used to either provide
trial parameter sets to feed into an optimiser as initial points, or importance weights to apply to each KPI.
The base class must define the following methods::

    def _get_sample_point(self):
    def generate_space_sample(self, *args, **kwargs):

Two concrete implementations of this class are provided: ``UniformSpaceSampler``, which performs a grid
search and ``DirichletSpaceSampler``, which samples random points from the Dirichlet distribution.

MCO Communicator
^^^^^^^^^^^^^^^^

The MCO Communicator must reimplement BaseMCOCommunicator and two methods:
``receive_from_mco()`` and ``send_to_mco()``. These two methods can use files,
stdin/stdout or any other trick to send and receive data between the MCO and
the BDSS running as a subprocess of the MCO to evaluate a single point.

Parameter factories
^^^^^^^^^^^^^^^^^^^

MCO parameter types also require a model and a factory per each type. Right
now, the only typo encountered is Range, but others may be provided in the
future, by MCOs that support them.

The parameter factory must inherit from ``BaseMCOParameterFactory`` and
reimplement::

    def get_identifier(self):
    def get_name(self):
    def get_description(self):

as in the case of data source. Then::

    def get_model_class(self):

must return a model class for the given parameter, inheriting from
``BaseMCOParameter``. This model contains the data the user can set, and is
relevant to the given parameter. For example, in the case of a Range, it might
specify the min and max value, as well as the starting value.

Notification Listeners
^^^^^^^^^^^^^^^^^^^^^^

Notification listeners are used to notify the state of the MCO to external
listeners, including the data that is obtained by the MCO as it performs the
evaluation. Communication to databases (for writing) and CSV/HDF5 writers are
notification listeners.

The notification listener requires a model (inherit from
``BaseNotificationListenerModel``), a factory (from
``BaseNotificationListenerFactory``) and a notification listener
(from ``BaseNotificationListener``). The factory requires, in addition to::

    def get_identifier(self):
    def get_name(self):
    def get_description(self):
    def get_model_class(self):

the method::

    get_listener_class()
     return the notification listener object class.

The NotificationListener class must reimplement the following methods, that
are invoked in specific lifetime events of the BDSS::

    def initialize(self):
        Called once, when the BDSS is initialized. For example, to setup the
        connection to a database, or open a file.

    def finalize(self):
        Called once, when the BDSS is finalized. For example, to close the
        connection to a database, or close a file.

    def deliver(self, event):
        Called every time the MCO generates an event. The event will be passed
        as an argument. Depending on the argument, the listener implements
        appropriate action. The available events are in the api module.

UI Hooks
^^^^^^^^

UI Hooks are callbacks that are triggered at some events during the lifetime
of the UI. It has no model. The factory must inherit from
``BaseUIHooksFactory``, and must reimplement ``get_ui_hooks_manager_class()``
to return a class inheriting from ``BaseUIHooksManager``. This class has
specific methods to be reimplemented to perform operations before and after
some UI operations.

Any ``BaseDriverEvents`` that are required to be delivered to a UI can be indicated
using the ``UIEventMixin`` class. The ``MCOStartEvent``, ``MCOProgressEvent`` and
``MCOFinishEvent`` are all examples of such objects.

Envisage Service Offers
^^^^^^^^^^^^^^^^^^^^^^^

A plugin can also define one or more custom visualization classes for the
GUI application ``force-wfmanager``, typically to either display data or
provide a tailor-made UI for a specific user. In which case, the plugin class
must inherit from ``force_bdss.core_plugins.service_offer_plugin.ServiceOfferExtensionPlugin``
, which is a child class of ``BaseExtensionPlugin``. Any UI subclasses
can then be made discoverable by ``force-wfmanager`` using the ``envisage``
``ServiceOffer`` protocol through the ``get_service_offer_factories`` method::

    def get_service_offer_factories(self):
        """A method returning a list user-made objects to be provided by this
        plugin as envisage ServiceOffer objects. Each item in the outer list is
        a tuple containing an Interface trait to be used as the ServiceOffer
        protocol and an inner list of subclass factories to be instantiated
        from said protocol.

        Returns
        -------
        service_offer_factories: list of tuples
            List of objects to load, where each tuple takes the form
            (Interface, [HasTraits1, HasTraits2..]), defining a Traits
            Interface subclass and a list of HasTraits subclasses to be
            instantiated as an envisage ServiceOffer.
        """

Make sure to import the module containing the data view class from inside
``get_service_offer_factories``: this ensures that running BDSS without a GUI
application doesn't import the graphical stack.

Custom UI classes
~~~~~~~~~~~~~~~~~

There are currently two types of custom UI object that may be contributed by a
plugin: ``IBasePlot`` and ``IContributedUI``. These interfaces represent requirements
for any UI feature that can be used to display MCO data or a present a simplified
workflow builder respectively.

Also, multiple types of plugin
contributed UI objects can be imported in the same call. For instance::

    def get_service_offer_factories(self):
        from force_wfmanager.ui import IBasePlot, IContributedUI
        from .example_custom_uis import PlotUI, ExperimentUI, AnalysisUI

        return [
            (IBasePlot, [PlotUI]),
            (IContributedUI, [ExperimentUI, AnalysisUI])
        ]
