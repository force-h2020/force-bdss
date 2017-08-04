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


def factory_id(producer, identifier):
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
    return _string_id(producer, "bundle", identifier)


def mco_parameter_id(producer, mco_identifier, parameter_identifier):
    """Creates an ID for an MCO parameter, so that it can be identified
    uniquely."""
    return _string_id(producer,
                      "bundle",
                      mco_identifier,
                      "parameter",
                      parameter_identifier)


def plugin_id(producer, identifier):
    """Creates an ID for the plugins. These must be defined, otherwise
    the envisage system will complain (but not break)
    """
    return _string_id(producer, "plugin", identifier)


def _string_id(*args):
    """Creates an id for a generic entity.

    Parameters
    ----------
    entity_namespace: str
        A namespace for the entity we want to address (e.g. "bundle")
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

    if not all(map(is_valid, args)):
        raise ValueError("One or more of the specified parameters was "
                         "invalid: {}".format(str(args)))

    return ".".join(["force", "bdss"]+list(args))
