from envisage.api import ServiceOffer
from traits.api import Instance, List, Interface

from force_bdss.api import BaseExtensionPlugin


class ServiceOffersPlugin(BaseExtensionPlugin):
    """A plugin which is able to contribute one or more user-made UI objects
    via the envisage ServiceOffer protocol. This plugin can handle
    multiple types of UI objects, via appropriate configuration of the
    object returned by get_service_offers"""

    #: Service offers provided by this plugin.
    service_offers = List(
        Instance(ServiceOffer),
        contributes_to='envisage.service_offers'
    )

    protocol = Instance(Interface)

    def get_service_offer_factories(self):
        """A method returning a tuple containing and Interface trait for a list
        of subclass factories provided by this plugin. The Interface trait is
        then used by _service_offers_default as a protocol to instantiate a
        ServiceOffer for each subclass.

        Example
        -------
        For a plugin which wants to offer the ContributedUI factories:
        `ExperimentUI` and `AnalysisUI` via the IContributedUI Interface,
        `get_contributed_uis` would be implemented as below

        >>> def get_service_offer_factories(self):
        ...     from force_wfmanager.ui.contributed_ui.i_contributed_ui \
        ...         import IContributedUI
        ...     return [
        ...         (IContributedUI, [ExperimentUI, AnalysisUI])
        ...     ]

        Where both `ExperimentUI` and `AnalysisUI` are subclasses of
        `ContributedUI`
        """
        raise NotImplementedError

    def _service_offers_default(self):
        """Method that imports all subclasses returned by get_service_offers
        as ServiceOffer objects using their associated Interface protocols
        """

        service_offers_factories = self.get_service_offer_factories()
        service_offers = []

        for protocol, factories in service_offers_factories:
            service_offers += [
                ServiceOffer(protocol=protocol, factory=factory)
                for factory in factories
            ]

        return service_offers
