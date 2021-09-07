import asyncio
import functools


def run_sync(func, *args, **kwargs):
    """Run a non-async function in a new thread and return an awaitable"""
    # Returning a coro
    return asyncio.get_event_loop().run_in_executor(
        None, functools.partial(func, *args, **kwargs)
    )
