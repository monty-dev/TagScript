import re
from inspect import isawaitable
from typing import Any, Awaitable, Callable, Union

import discord

__all__ = ("escape_content", "maybe_await", "DPY2")

DPY2 = discord.version_info >= discord.VersionInfo(major=2, minor=0, micro=0, releaselevel='alpha', serial=0)

pattern = re.compile(r"(?<!\\)([{():|}])")


def _sub_match(match: re.Match) -> str:
    return "\\" + match.group(1)


def escape_content(string: str) -> str:
    """
    Escapes given input to avoid tampering with engine/block behavior.

    Returns
    -------
    str
        The escaped content.
    """
    if string is None:
        return
    return pattern.sub(_sub_match, string)


async def maybe_await(func: Union[Callable[..., Any], Awaitable[Any]], *args, **kwargs) -> Any:
    """
    Await the given function if it is awaitable or call it synchronously.

    Returns
    -------
    Any
        The result of the awaitable function.
    """
    value = func(*args, **kwargs)
    return await value if isawaitable(value) else value
