import asyncio
import inspect
from asyncio import Event
from typing import Callable


class EventBus:
    def __init__(self):
        self._event_dict = dict()

    async def on(self, event_name: str, fn: Callable):
        event = self._get_event(event_name)
        while True:
            await event.wait()
            print("event fired")
            result = fn(*event.args, **event.kwargs)
            if inspect.isawaitable(result):
                await result

            # Since the callback function is likely a synchronous method,
            # we must perform an await here to allow other tasks to execute.
            await asyncio.sleep(0.1)
            event.clear()

    def trigger(self, event_name: str, *args, **kwargs):
        event = self._get_event(event_name)

        event.args = args
        event.kwargs = kwargs
        event.set()

    def _get_event(self, event_name: str):
        if event_name in self._event_dict:
            print("event already inited...")
            event = self._event_dict.get(event_name)
        else:
            print(f"need to init a new event for {event_name}")
            event = Event()
            self._event_dict[event_name] = event
        return event


def a_sync_callback(data):
    print(f"A sync callback with data {data} is triggered")


async def a_async_callback(data):
    await asyncio.sleep(1)
    print(f"An async callback with data {data} is triggered")


async def main():
    event_bus = EventBus()
    task_one = asyncio.create_task(event_bus.on("some_event", a_async_callback))
    task_two = asyncio.create_task(event_bus.on("some_event", a_sync_callback))

    event_bus.trigger("some_event", {id: 1})
    await asyncio.wait([task_one, task_two], timeout=10.0)


if __name__ == "__main__":
    asyncio.run(main())
