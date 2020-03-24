FORCE BDSS Design
=================

The BDSS is an Envisage/Task application. it uses tasks to manage the plugin
system, with stevedore to manage the additions.

The main class is ``BDSSApplication``, which is in charge of loading the plugins,
and also adding the relevant core plugins to make the whole system run.
Specifically it loads:

- The ``FactoryRegistryPlugin``, which is where all external plugins will put
  their classes.
- Depending on the --evaluate switch, a relevant execution plugin:
    - ``OptimizeOperation``: Invokes the MCO.
    - ``EvaluateOperation``: performs a single point evaluation, that is,
      executes the pipeline only once.

Application
-----------

The ``BDSSApplication`` is an ``envisage.Application`` subclass,
which contains the following structure:

.. image:: _images/bdss_application_design.svg

At the ``BDSSApplication`` level, there are three main attributes of type:

- ``WorkflowFile``: contains the ``Workflow`` object, as well as the ability to
  read, write from file
- ``IOperation``: determines the operation that will be performed by the BDSS
- ``IFactoryRegistry``: contains references to all ``IFactory`` classes that
  are contributed by currently installed plugins. This object is constructed from
  by the ``BDSSApplication``, using the Envisage plugins installed in the local
  environment, but is actually used by ``WorkflowReader`` to instantiate serialised
  ``Workflow`` objects from file.

Factories
---------

MCO Factory Classes
~~~~~~~~~~~~~~~~~~~

.. image:: _images/mco_classes_design.svg

The ``BaseMCOFactory`` fulfills the ``IMCOFactory`` interface, and is therefore able to be
contributed and subsequently located by the ``BaseExtensionPlugin`` and ``FactoryRegistryPlugin``
classes respectively. It is able to construct both ``BaseMCO`` and ``BaseMCOModel``
subclasses and also contains references to a list of objects that fulfill the ``IMCOParameterFactory``
interface.

BaseMCO Class
~~~~~~~~~~~~~

Current classes and brief description
-------------------------------------



Note: the design requiring the ``--evaluate`` switch assumed a "Dakota" model of
execution (external process controlled by Dakota). In the current Enthought Example plugin
we use both the ``--evaluate`` strategy and direct control, where all the
calculation is performed without spawning additional processes other than the
initial ``force_bdss``.

The packages ``data_sources``, ``mco``, ``notification_listeners`` and ``ui_hooks``, as well as
the ``base_extension_plugin``, contain the base classes that plugin developers need
to use in order to write a plugin. They have been coded to be as error tolerant
as possible, and deliver robust error messages as much as possible.

The ``io`` package contains the reader and writer for the model. It simply
serializes the model objects and dumps them to JSON, or vice-versa. Note that
the reader requires the factory registry, because you can't load entities
from the file if you don't have the appropriate plugin, as only the plugin
knows the model structure and can therefore take the JSON content and apply
it to the model object.

The ``core_plugins`` contains fundamental plugins that are considered part of a
"standard library", providing common data sources, MCOs and other relevant objects.

Finally, ``core`` contains:

- base classes for a few entities that are reused for the plugins.
- the ``DataValue`` entity. This is the "exchange entity" between data sources.
  It is a value that also contains the type, the accuracy, and so on. It can
  refer to anything: a float, an array, a string, etc.
- ``Workflow`` model object, representing the entire state of the BDSS.
- ``input/output_slot_info`` contain the ``_bound_`` information for slots. A
  ``DataSource`` provides slots (see slot module) but these are not bound to a
  specific "variable name". The ``SlotInfo`` classes provide this binding.
- ``execution_layer`` contains the ``ExecutionLayer`` class, which provide the actual machinery that runs the pipeline.
- ``verifier`` contains a verification function that checks if the workflow can
  run or has errors.

Workflow Files
--------------

A ``Workflow`` object can be instantiated from an appropriately formatted workflow JSON file.
Typically the structure of this JSON represents a serialised version of each object contained
within the ``Workflow``. Currently the ``WorkflowReader`` supports two file versions: 1 and 1.1.
There are only minor differences between both versions:

1. ``Workflow.mco_model`` attribute data stored under ``mco`` key in version 1 vs ``mco_model`` key in 1.1
2. ``Workflow.execution_layers`` attribute data represented as a list of lists in version 1 vs
   a list of dictionaries in version 1.1. In version 1, each element in the outer list implicitly represents
   an execution layer, whilst each element in the the inner list represents the serialised status of a
   ``DataSourceModel`` instance. In version 1.1, we explicitly include the status of each ``ExecutionLayer``
   instance in the outer list, and therefore each dictionary element is also expected to contain a
   ``data_sources`` key with a list of ``DataSourceModel`` statuses.

Future directions
-----------------

The future design will probably need to address the following:

- Check if the ``--evaluate`` strategy and design is still relevant. More MCOs are
  needed for reasonable conclusions.
- IWM is going to provide a strict description of types (``emmc-info``, previously
  known as ``simphony``). Currently, all type entries in the e.g. slots are simple
  strings as a workaround. This is supposed to change once IWM provides a
  comprehensive set of types.
- The project is now at a stage where plugins can be developed, and real
  evaluations can be performed. We can solve the current toy cases, but real
  cases and UI requirements may promote the need for additional requirements.
