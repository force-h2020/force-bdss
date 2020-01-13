Design
------

The application is based on four entities, as written in the introduction:

- Multi Criteria Optimizer (MCO)
- Data Sources
- Notification Listeners
- UI Hooks

There are a few core assumptions about each of these entities:

- The ``MCO`` provides numerical values and injects them into a pipeline
  made of multiple layers. Each layer is composed of multiple data sources.
  The ``MCO`` can execute this pipeline directly, or indirectly by invoking
  the ``force_bdss`` with the option ``--evaluate``. This invocation will produce,
  given a vector in the input space, a vector in the output space.
- The ``DataSources`` are entities that are arranged in layers. Each ``DataSource`` has
  inputs and outputs, called slots. These slots may depend on the configuration
  options of the specific data source. The pipeline is created by binding
  data sources outputs on the layers above with the data sources inputs of a
  given layer. Each output can be designated as a KPI and thus be transmitted
  back to the ``MCO`` for optimization.
- The ``NotificationListener`` listens to the state of the ``MCO`` (Started/New step
  of the computation/Finished). It can be a remote database which is filled
  with the ``MCO`` results during the computation (e.g. the GUI ``force_wfmanager``
  has a notification listener in order to fill the result table).
- UI Hooks permit to define additional operations which will be executed
  at specific moments in the UI lifetime (before and after execution of the
  BDSS, before saving the workflow). Those operations won't be executed by the
  command line interface of the BDSS.

The result can be represented with the following data flow

1. The ``MCO`` produces and, potentially by means of a ``MCOCommunicator`` (if the
   execution model is based on invoking ``force_bdss --evaluate``),
   injects a given vector of MCO parameter values in the pipeline.
2. These values are passed to one or more ``DataSources``, organised in ``ExecutionLayers``,
   each performing some computation or data extraction and produces results.
   ``ExecutionLayers`` are executed in order from top to bottom. There is no order among
   ``DataSources`` on the same layer.
3. Results that have been classified as KPIs are then returned to the MCO
   (again, potentially via the ``MCOCommunicator``).
4. The KPI values are then sent to the ``NotificationListeners`` with the
   associated ``MCOParameter`` values
5. The cycle repeats until all evaluations have been performed.


Current classes and brief description
-------------------------------------

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
