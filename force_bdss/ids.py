import six


class ExtensionPointID:
    """The envisage extension points ids for the bundles ExtensionPoints.
    These are populated by the envisage plugins.

    The plugin developer generally does not have to handle these identifiers,
    as they just have to reimplement the plugin base class and implement
    the appropriate default methods.
    """
    MCO_BUNDLES = 'force.bdss.mco.bundles'
    DATA_SOURCE_BUNDLES = 'force.bdss.data_source.bundles'
    KPI_CALCULATOR_BUNDLES = 'force.bdss.kpi_calculator.bundles'


def bundle_id(producer, identifier):
    """Creates an id for the bundle.

    Parameters
    ----------
    producer: str
        the company or research institute unique identifier (e.g. "enthought")
    identifier: str
        A unique identifier for the bundle. The producer has authority and
        control over the uniqueness of this identifier.

    Returns
    -------
    str: an identifier to be used in the bundle.
    """
    def is_valid(entry):
        return (
            isinstance(entry, six.string_types) and
            " " not in entry and
            len(entry) != 0)

    if not all(map(is_valid, [producer, identifier])):
        raise ValueError("Invalid parameters specified.")

    return "force.bdss.bundles.{}.{}".format(producer, identifier)
