import asyncio
from asyncio import Condition
from enum import Enum


class ConnectionState(Enum):
    WAIT_INIT = 0
    INITIALIZING = 1
    INITIALIZED = 2


class Connection:
    def __init__(self):
        self._state = ConnectionState.WAIT_INIT
        self._condition = Condition()

    async def initialize(self):
        print("initialize: Preparing initialize the connection.")
        await self._change_state(ConnectionState.INITIALIZING)
        await asyncio.sleep(5)
        print("initialize: Connection initialized")
        await self._change_state(ConnectionState.INITIALIZED)

    async def execute(self, query: str):
        async with self._condition:
            print("execute: Waiting for connection initialized")
            await self._condition.wait_for(self._is_initialized)
            print(f"execute: Connection initialized, executing query: {query}")
            await asyncio.sleep(5)
            print("execute: Execute finished.")

    async def _change_state(self, state: ConnectionState):
        print(f"_change_state: Will change state from {self._state} to {state}")
        self._state = state
        print("_change_state: Change the state and notify all..")
        async with self._condition:
            self._condition.notify_all()

    def _is_initialized(self):
        if self._state is not ConnectionState.INITIALIZED:
            print("_is_initialized: The connection is not initialized.")
            return False
        print("_is_initialized: The connection is ready.")
        return True


async def main():
    connection = Connection()
    task_one = asyncio.create_task(connection.execute("SELECT * FROM table"))
    task_two = asyncio.create_task(connection.execute("SELECT * FROM other_table"))

    asyncio.create_task(connection.initialize())
    await asyncio.gather(task_one, task_two)


if __name__ == "__main__":
    asyncio.run(main())
