Workflow
--------

The ``Workflow`` contains a full description of the system to be optimised, the optimisation
proceedure and any listener objects that are expected to react on events that are
created during runtime.

As shown above, the ``Workflow`` object of the application is based on three entities:

- Multi Criteria Optimizer (MCO)
- Data Sources
- Notification Listeners

Addtionally, messages can be sent and recieved between the CLI ``force_bdss`` application
and the ``force_wfmanager`` GUI via a subset of notification listener, known as a
'UI Hook'.

There are a few core assumptions about each of these entities:

- The MCO provides numerical values and injects them into a pipeline
  made of multiple layers. Each layer is composed of multiple data sources.
  The MCO can execute this pipeline directly, or indirectly by invoking
  the ``force_bdss`` with the option ``--evaluate``. This invocation will produce,
  given a vector in the input space, a vector in the output space.
- The Data Sources are entities that are arranged in layers. Each Data Source has
  inputs and outputs, called slots. These slots may depend on the configuration
  options of the specific data source. The pipeline is created by binding
  data sources outputs on the layers above with the data sources inputs of a
  given layer. Each output can be designated as a KPI and thus be transmitted
  back to the MCO for optimization.
- A Notification Listener listens to the state of the MCO (Started/New step
  of the computation/Finished). It can be a remote database which is filled
  with the MCO results during the computation (e.g. the GUI ``force_wfmanager``
  has a notification listener in order to fill the result table).
- UI Hooks permit to define additional operations which will be executed
  at specific moments in the UI lifetime (before and after execution of the
  BDSS, before saving the workflow). Those operations won't be executed by the
  command line interface of the BDSS.

The result can be represented with the following data flow

1. The MCO produces and, potentially by means of a ``MCOCommunicator`` (if the
   execution model is based on invoking ``force_bdss --evaluate``),
   injects a given vector of MCO parameter values in the pipeline.
2. These values are passed to one or more Data Sources, organised in layers,
   each performing some computation or data extraction and produces results.
   The layers are executed in order from top to bottom. There is no order among
   Data Sources on the same layer.
3. Results that have been classified as KPIs are then returned to the MCO
   (again, potentially via the ``MCOCommunicator``).
4. The KPI values are then sent to the Notification Listeners with the
   associated MCO parameter values.
5. The cycle repeats until all evaluations have been performed.
