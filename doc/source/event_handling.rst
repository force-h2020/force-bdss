Event Handling
--------------

The ``BaseDriverEvent`` class is the main object used to relay messages internally between
components of the ``BDSSApplication``. It can also be serialized in order to be passed between
external programs (i.e. the ``force_wfmanager``) as a JSON.

Any events that are created during runtime are propagated through the ``Workflow`` object
hierarchy, up to the ``BaseOperation`` class that is being performed by the ``BDSSApplication``,
before finally being broadcast to all ``BaseNotificationListener`` classes present. Consequently,
the ``BaseModel`` class contains an ``event`` attribute, as well as a ``notify`` method that is used to
set it. Listeners can then detect changes in any ``BaseModel.event`` subclass, and
process the new event accordingly.

.. image:: _images/event_handling.svg

Any actions that are required to be performed upon notification of a specific ``BaseDriverEvent``
subclass are handled by the ``BaseNotificationListener.deliver`` method.

In this way, we can also use ``BaseDriverEvents`` to control the progress of an MCO run,
since after every broadcast, the ``OptimizeOperation`` checks its run time status to see whether
the event has triggered a MCO 'pause' or 'stop' signal.

Additionally, the ``BaseDataSource._run`` method shadows the ``BaseDataSource.run`` method in order to
signal the beginning and end of a data source execution. By doing so,
we are able to pause and stop and MCO run between each ``run`` method invocation, which represents
a black box operation.