from envisage.api import ServiceOffer
from traits.api import Instance, List, Interface

from force_bdss.api import BaseExtensionPlugin


class ServiceOffersPlugin(BaseExtensionPlugin):
    """A plugin which is able to contribute one or more user-made
    subclasses via the envisage ServiceOffer protocol. This plugin can
    handle multiple types of objects, via appropriate configuration of the
    object returned by get_service_offers"""

    #: Service offers provided by this plugin.
    service_offers = List(
        Instance(ServiceOffer),
        contributes_to='envisage.service_offers'
    )

    protocol = Instance(Interface)

    def get_service_offer_factories(self):
        """A method returning a list user-made objects to be provided by this
        plugin as envisage ServiceOffer objects. Each item in the outer list is
        a tuple containing an Interface trait to be used as the ServiceOffer
        protocol and an inner list of subclass factories to be instantiated
        from said protocol.

        Returns
        -------
        service_offer_factories: list of tuples
            List of objects to load, where each tuple takes the form
            (Interface, [HasTraits1, HasTraits2..]), defining a Traits
            Interface subclass and a list of HasTraits subclasses to be
            instantiated as an envisage ServiceOffer.

        Example
        -------
        This example showcases a situation where a plugin wants contribute
        subclasses of UI objects defined in force-wfmanager. Specifically,
        to offer the ContributedUI factories: `ExperimentUI` and `AnalysisUI`
        via the IContributedUI Interface. In which case, `get_contributed_uis`
        would be implemented as below

        >>> def get_service_offer_factories(self):
        ...     from force_wfmanager.ui import IContributedUI
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
