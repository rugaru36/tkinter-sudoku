import asyncio
# from contextlib import suppress
from threading import Thread
from time import sleep
from typing import Callable, Final, Never


class Timer:
    def __init__(self, delay: int, callback: Callable[[], None] | None = None, name: str | None = None):
        self._loop: Final = asyncio.get_event_loop()
        self._name: Final = name
        self._on_tick_cb: Final = callback
        self._task: asyncio.Task[Never] | None = None
        self._delay: Final = delay
        self._is_running: bool = False
        self._thread: Thread | None = None

    def start(self):
        if not self._is_running:
            self._is_running = True
            self._init_thread()

    def stop(self):
        self._is_running = False

    def _init_thread(self):
        self._thread = Thread(name=self._name)
        self._thread.run = self._tick_iterations
        self._thread.daemon = True
        if self._name:
            self._thread.name = self._name
        self._thread.start()

    def _tick_iterations(self):
        while self._is_running:
            sleep(self._delay)
            if self._is_running and self._on_tick_cb is not None:
                self._on_tick_cb()
