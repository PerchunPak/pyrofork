import asyncio
import datetime as dt
import logging
import typing as t
from types import TracebackType

logger = logging.getLogger(__name__)


class _FloodWaiterSingleton(type):
    _instances: dict[str, "FloodWaiter"] = {}

    @t.override
    def __call__(cls, name: str, backoff: int, threshold: float) -> "FloodWaiter":
        if name not in cls._instances:
            instance = super(_FloodWaiterSingleton, cls).__call__(name, threshold)
            cls._instances[name] = instance

        instance = cls._instances[name]
        instance.add_backoff(backoff)
        return instance


@t.final
class FloodWaiter(metaclass=_FloodWaiterSingleton):
    """Global backoff handler.

    Globally locks queries to specific invoke events. Also keeps track of what
    was the max backoff requested, and sleeps for that.
    """

    def __init__(self, name: str, threshold: float) -> None:
        self._name = name
        self._threshold = threshold
        self._lock = asyncio.Lock()
        self._sleep_until = dt.datetime.now(tz=dt.UTC) - dt.timedelta(seconds=1)

    def add_backoff(self, backoff: int) -> None:
        sleep_until = dt.datetime.now(tz=dt.UTC) + dt.timedelta(seconds=backoff)
        if sleep_until > self._sleep_until:
            self._sleep_until = sleep_until

    async def acquire(self) -> None:
        async with self._lock:
            to_sleep = (self._sleep_until - dt.datetime.now(tz=dt.UTC)).total_seconds()

            if to_sleep <= 0:
                return
            if to_sleep > self._threshold:
                raise TimeoutError(
                    f"Tried to sleep until {self._sleep_until} ({to_sleep} "
                    + f"seconds), but threshold is {self._threshold}"
                )

            log_repr = self._sleep_until.astimezone().strftime("%H:%M:%S %Y-%m-%d")
            logger.info(f"Sleeping until {log_repr} for invoke request {self._name}")
            await asyncio.sleep(to_sleep)

    async def __aenter__(self) -> None:
        await self.acquire()

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc: BaseException | None,
        _tb: TracebackType | None,
    ) -> None:
        pass
