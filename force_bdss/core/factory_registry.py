from traits.api import HasStrictTraits, Instance, List, provides

from force_bdss.core.i_factory_registry import IFactoryRegistry
from force_bdss.data_sources.i_data_source_factory import IDataSourceFactory
from force_bdss.mco.i_mco_factory import IMCOFactory
from force_bdss.notification_listeners.i_notification_listener_factory import (  # noqa: E501
    INotificationListenerFactory
)
from force_bdss.ui_hooks.i_ui_hooks_factory import IUIHooksFactory


@provides(IFactoryRegistry)
class FactoryRegistry(HasStrictTraits):
    """ Default factory registry for the application.
    """

    #: A List of the available Multi Criteria Optimizers.
    mco_factories = List(Instance(IMCOFactory))

    #: A list of the available Data Sources.
    data_source_factories = List(Instance(IDataSourceFactory))

    #: Notification listeners are pluggable entities that will listen
    #: to MCO events and act accordingly.
    notification_listener_factories = List(
        Instance(INotificationListenerFactory)
    )

    #: UI Hooks are pluggable entities holding methods that are called
    #: at specific moments in the UI application lifetime. They can be used
    #: to inject special behaviors at those moments.
    ui_hooks_factories = List(Instance(IUIHooksFactory))

    def data_source_factory_by_id(self, id):
        """Finds a given data source factory by means of its id.
        The ID is as obtained by the function factory_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the factory_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for ds in self.data_source_factories:
            if ds.id == id:
                return ds
        raise KeyError(id)

    def mco_factory_by_id(self, id):
        """Finds a given Multi Criteria Optimizer (MCO) factory by means of
        its id. The ID is as obtained by the function factory_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the factory_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for mco in self.mco_factories:
            if mco.id == id:
                return mco
        raise KeyError(id)

    def mco_parameter_factory_by_id(self, mco_id, parameter_id):
        """Retrieves the MCO parameter factory for a given MCO id and
        parameter id.

        Parameters
        ----------
        mco_id: str
            The MCO identifier string
        parameter_id: str
            the parameter identifier string

        Returns
        -------
        An instance of BaseMCOParameterFactory.

        Raises
        ------
        KeyError:
            if the entry is not found
        """
        mco_factory = self.mco_factory_by_id(mco_id)

        for factory in mco_factory.parameter_factories:
            if factory.id == parameter_id:
                return factory

        raise KeyError(parameter_id)

    def notification_listener_factory_by_id(self, id):
        """Finds a given notification listener by means of its id.
        The ID is as obtained by the function factory_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the factory_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for nl in self.notification_listener_factories:
            if nl.id == id:
                return nl

        raise KeyError(id)
