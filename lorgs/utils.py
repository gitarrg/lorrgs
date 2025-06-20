"""A Collection of very generic Helper Functions."""

# pylint: disable=invalid-name
from __future__ import annotations

import asyncio
import datetime
import functools
import itertools
import typing
from operator import attrgetter


T = typing.TypeVar("T")
U = typing.TypeVar("U")


def chunks(lst: list[T], n: int) -> typing.Generator[list[T], None, None]:
    """Yield successive n-sized chunks from lst."""
    if n <= 0:  # special case to allow unchucked
        yield lst
        return

    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def format_time(timestamp: int) -> str:
    """Format a time/duration.

    Args:
        timestamp: time in milliseconds

    Example:
        >>> format_time(272000)
        "4:32"

    """
    sign = ""
    if timestamp < 0:
        sign = "-"
        timestamp = abs(timestamp)

    duration = datetime.timedelta(milliseconds=timestamp)

    duration_str = str(duration)  # "0:05:12.00000"
    duration_str = duration_str[2:7]
    return sign + duration_str


def format_big_number(num: float) -> str:
    """Formats a large number into a readable format.

    Example:
        >>> utils.format_big_number(12345)
        '123.35k'

    Args:
        num (float): The number to be formatted

    Returns:
        str: the formatted string

    """
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    suffix = ["", "k", "m", "g", "t", "p"][magnitude]
    return f"{num:0.2f}{suffix}"


def slug(text: str, space="", delete_chars="(),'-") -> str:
    """Slugifies an input text.

    >>> utils.slug("Hey Test Number 2", space="|")
    'hey|test|number|2'

    Args:
        text (str): the text to slugify
        space (str, optional): character to use in place of whitespace. Defaults to "".
        delete_chars (str, optional): Characters to remove. Defaults to "(),'-".

    Returns:
        str: the slugified text.
    """
    text = text.lower()
    for c in delete_chars:
        text = text.replace(c, "")
    text = text.replace(" ", space)
    return text


def to_snake_case(name) -> str:
    """Convert CamelCase to snake case."""
    return "".join("_%s" % c if c.isupper() else c for c in name).strip("_").lower()


def str_int_list(string: str, sep=".") -> list[int]:
    """Converts string-list of intergers into an actual list.

    Example:
        >>> str_int_list("2/4/8/16", sep="/")
        [2, 4, 8, 16]

    """
    if not string:
        return []

    return [int(v) for v in string.split(sep)]


def rename_dict_keys(data: dict[str, typing.Any], names: dict[str, str], reverse=False) -> dict[str, typing.Any]:
    """Renames keys in a dictornary.

    Examples:
    >>> d = { "foo": 1234, "b": "value" }
    >>> k = { "foo": "f", "bar": "b" }
    >>> rename_dict_keys(d, k)
    {'f': 1234, 'b': 'value'}
    >>> rename_dict_keys(d, k, reverse=True)
    {'foo': 1234, 'bar': 'value'}

    """
    name_map = dict(names)

    if reverse:
        name_map = {v: k for k, v in name_map.items()}

    return {name_map.get(k, k): v for k, v in data.items()}


def flatten(values: typing.Iterable[typing.Iterable[T]]) -> list[T]:
    """Flattens a list of lists into a single large list.

    https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists

    Example:
        >>> flatten( [[a, b], [c, d]] )
        [a, b, c, d]
    """
    return list(itertools.chain.from_iterable(values))


def as_list(func: typing.Callable[[U], typing.Generator[T, None, None]]) -> typing.Callable[[U], list[T]]:
    """Wrap a Generator to return a list."""

    @functools.wraps(func)
    def wrapped(*args: typing.Any, **kwargs: typing.Any) -> list[T]:
        return list(func(*args, **kwargs))

    return wrapped


def uniqify(iterable: typing.Iterable[T], key: typing.Callable[[T], typing.Hashable]) -> list[T]:
    """Return unique Items from a list.

    Args:
        iterable (iterable[T]): The Source Items
        key (callable[T], str]): Key Generator Function, taking a single Item

    Returns:
        list[T]: filtered list
    """
    d = {key(item): item for item in iterable}
    return list(d.values())


def find(predicate: typing.Callable[[T], typing.Any], seq: typing.Iterable[T]) -> typing.Optional[T]:
    """A helper to return the first element found in the sequence
    that meets the predicate. For example: ::

        member = discord.utils.find(lambda m: m.name == 'Mighty', channel.guild.members)

    would find the first :class:`~discord.Member` whose name is 'Mighty' and return it.
    If an entry is not found, then ``None`` is returned.

    This is different from :func:`py:filter` due to the fact it stops the moment it finds
    a valid entry.

    Parameters
    -----------
    predicate
        A function that returns a boolean-like result.
    seq: iterable
        The iterable to search through.
    """

    for element in seq:
        if predicate(element):
            return element
    return None


def get(iterable: typing.Iterable[T], **attrs) -> typing.Optional[T]:
    r"""A helper that returns the first element in the iterable that meets
    all the traits passed in ``attrs``. This is an alternative for
    :func:`~discord.utils.find`.

    When multiple attributes are specified, they are checked using
    logical AND, not logical OR. Meaning they have to meet every
    attribute passed in and not one of them.

    To have a nested attribute search (i.e. search by ``x.y``) then
    pass in ``x__y`` as the keyword argument.

    If nothing is found that matches the attributes passed, then
    ``None`` is returned.

    Examples
    ---------

    Basic usage:

    .. code-block:: python3

        member = discord.utils.get(message.guild.members, name='Foo')

    Multiple attribute matching:

    .. code-block:: python3

        channel = discord.utils.get(guild.voice_channels, name='Foo', bitrate=64000)

    Nested attribute matching:

    .. code-block:: python3

        channel = discord.utils.get(client.get_all_channels(), guild__name='Cool', name='general')

    Parameters
    -----------
    iterable
        An iterable to search through.
    \*\*attrs
        Keyword arguments that denote attributes to search with.
    """

    # global -> local
    _all = all
    attrget = attrgetter

    # Special case the single element call
    if len(attrs) == 1:
        k, v = attrs.popitem()
        pred = attrget(k.replace("__", "."))
        for elem in iterable:
            if pred(elem) == v:
                return elem
        return None

    converted = [(attrget(attr.replace("__", ".")), value) for attr, value in attrs.items()]

    for elem in iterable:
        if _all(pred(elem) == value for pred, value in converted):
            return elem
    return None


def run_in_executor(_func):
    """Wraps a function to run inside the asyncio default executor.

    We can use this to make blocking functions async (more or less)

    """

    @functools.wraps(_func)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        func = functools.partial(_func, *args, **kwargs)
        return loop.run_in_executor(executor=None, func=func)

    return wrapped


def get_nested_key(d: dict, keys: typing.Iterable[str]) -> typing.Any:
    """Get a nested key from a dictionary.

    Args:
        d (dict): The dictionary to search
        keys (iterable): The keys to search for

    Returns:
        Any: The value of the nested key, or None if not found
    """
    for key in keys:
        d = d.get(key)
        if d is None:
            return None
    return d
