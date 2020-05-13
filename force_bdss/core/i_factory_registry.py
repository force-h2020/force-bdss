#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Interface


class IFactoryRegistry(Interface):
    """ Interface for factory registries. """

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
