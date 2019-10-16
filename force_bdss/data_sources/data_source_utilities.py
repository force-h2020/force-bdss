from logging import getLogger

logger = getLogger(__name__)


def trait_merge_check(source, target, name, ignore_default=False):
    """Check whether attribute on target can be merged with the
    same attribute on source. As a rule, this is allowed only when
    both attributes share the same value, except if
    ignore_default==True, then it is also allowed if the
    source attribute has not been changed from its default value.

    Parameters
    ----------
    source, target: objects
        Object instances to have attributes compared
    name: str
        Name of an attribute to check
    ignore_default: bool, optional, default: False
        Whether or not to ignore the attribute on source if it is
        equal to its default value. Note: this will not be performed
        if attribute does not have a default.
    """

    source_attr = getattr(source, name)
    target_attr = getattr(target, name)

    # If ignore_default perform a check to see whether attribute on
    # source is its default value, and skip cross check if so
    if ignore_default:
        try:
            if source_attr == source.trait(name).default:
                return True
        except AttributeError:
            pass

    # Return attribute equality check
    return target_attr == source_attr


def attr_checker(source, target, attributes, ignore_default=False):
    """Performs a `trait_merge_check` between source and target
    objects for each attribute listed in `attributes`. Returns a list
    of attributes that fail this check.

    Parameters
    ----------
    source, target: objects
        Object instances to perform attribute checks on
    attributes: str or list of str
        An attribute or list of attributes used to check merge
        eligibility of source and target objects
    ignore_default: bool, optional, default: False
        Whether or not to ignore any attributes on source listed in
        attributes that are are equal to their default values

    Returns
    -------
    failed_attr: list of str
        Names of attributes on source and target that fail a
        merge check
    """

    # Ensure attributes argument is in an iterable format
    if attributes is None:
        attributes = []
    elif isinstance(attributes, str):
        attributes = [attributes]
    else:
        attributes = list(attributes)

    failed_attr = []

    # Iterate through attributes list
    for attr_name in attributes:
        if not trait_merge_check(source, target, attr_name, ignore_default):
            failed_attr.append(attr_name)

    return failed_attr


def sync_trait_with_check(source, target, name, attributes=None,
                          ignore_default=False):
    """Sync an attribute on a HasTraits object (target) with that of another
    HasTraits object (source). Performs the same function as `sync_trait`
    method, but with some extra logic checks on on selected attributes
    supplied by `attributes`. These checks are designed to determine
    whether both objects possess a similar enough state to sync the
    `name` attribute.

    Parameters
    ----------
    source, target: HasTraits
        HasTraits instances to have an attribute synchronised
    name: str
        Name of an attribute on both source and target to be synced
    attributes: str or list of str, optional
        An attribute or list of attributes to check equivalence on both
        source and target objects
    ignore_default: bool, optional, default: False
        Whether or not to ignore any attributes on source listed in
        attributes that are are equal to their default values

    Raises
    -----
    RuntimeError, if any attribute checks fail
    """

    # Obtain names of any attributes in `attr_check` on both source and
    # target that fail a `trait_merge_check`
    failed_attr = attr_checker(source, target, attributes,
                               ignore_default=ignore_default)

    if failed_attr:
        attr_name = failed_attr[0]
        error_msg = (
            "The {} attribute of source {} ({}) doesn't match the "
            "target {} ({}).".format(
                attr_name, source, getattr(source, name),
                target, getattr(target, name)
            )
        )
        logger.exception(error_msg)
        raise RuntimeError(error_msg)

    # Sync attribute `name` on target with that of source
    source.sync_trait(name, target, mutual=False)
