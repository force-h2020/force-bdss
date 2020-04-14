FORCE BDSS Design
=================

The BDSS is an Envisage/Task application. it uses tasks to manage the plugin
system, with stevedore to manage the additions.

.. toctree::
        BDSS Application <bdss_application>
        Class Diagrams <class_diagrams>
        Workflow representation <workflow_schema>
        Event Handling <event_handling>
        Verification <verification>
        Package Structure <package_structure>

Future directions
-----------------

The future design will probably need to address the following:

- Check if the ``--evaluate`` strategy and design is still relevant. More MCOs are
  needed for reasonable conclusions.
- IWM is going to provide a strict description of types (``osp-core``, previously
  known as ``simphony``). Currently, all type entries in the e.g. slots are simple
  strings as a workaround. This is supposed to change once IWM provides a
  comprehensive set of types.
- The project is now at a stage where plugins can be developed, and real
  evaluations can be performed. We can solve the current toy cases, but real
  cases and UI requirements may promote the need for additional requirements.
