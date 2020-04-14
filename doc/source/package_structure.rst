Package Structure
-----------------

As well as a command line program, the BDSS also comes with a ``force_bdss`` package containing
objects required by plugin developers. These should be publicly accessed through the ``force_bdss.api``
module, but a brief explanation of the internal structure is provided below.

The ``data_sources``, ``mco``, ``notification_listeners`` and ``ui_hooks`` packages, and
the ``base_extension_plugin`` class, contain all the base classes that plugin developers need
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
- ``execution_layer`` contains the ``ExecutionLayer`` class, which provides the actual machinery
  that runs the pipeline.
- ``verifier`` contains a verification function that checks if the workflow can
  run or has errors.