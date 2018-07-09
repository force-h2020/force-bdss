Design
------

The application is based on five entities, as written in the introduction:

- Multi Criteria Optimizer (MCO)
- DataSources
- Notification Listeners
- UI Hooks

There are a few core assumptions about each of these entities:

- The MCO design must honor the execution model of Dakota, that is, spawn
  a secondary process that performs a computation starting from a given set
  of input parameters, and produces a resulting set of output parameters.
  In our code, this secondary process is ``force_bdss`` itself, invoked with
  the option ``--evaluate``.
- The DataSources are entities that, given the MCO parameters, provide some
  numerical result.
- The Notification Listener listens to the state of the MCO (Started/New step
  of the computation/Finished). It can be a remote database which is filled
  with the MCO results during the computation (e.g. the GUI ``force_wfmanager``
  has a notification listener in order to fill the result table).
- UI Hooks permit to define additional operations which will be executed
  at specific moments in the UI lifetime (before and after exectution of the
  bdss, before saving the workflow). Those operations won't be executed by the
  command line interface of the bdss.


The result can be represented with the following data flow


1. The MCO produces and, by means of a Communicator, injects...
2. ...DataSourceParameters, that are passed to...
3. one or more DataSources, organised in layers,
   each performing some computation or data extraction and produces. Layers
   are executed in order from top to bottom. Results that are classified as
   KPIs are then returned to...
4. The MCO via the Communicator.
5. The KPI values are then sent to the notification listeners with the
   associated MCO parameters values
