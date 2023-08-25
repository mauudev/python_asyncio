import asyncio
from random import randint, random


class AsyncException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super(*args, **kwargs)

    def __str__(self):
        return self.message


async def some_coro(name):
    print(f"Coroutine {name} begin to run")
    value = random()

    delay = randint(1, 4)
    await asyncio.sleep(delay)
    if value > 0.5:
        raise AsyncException(f"Something bad happen after delay {delay} second(s)")
    print(f"Coro {name} is Done. with delay {delay} second(s)")
    return value


async def main():
    aws, results = [], []
    for i in range(3):
        aws.append(asyncio.create_task(some_coro(f"name-{i}")))

    # When the value of return_exception is True, exceptions thrown by background tasks
    # will not affect the execution of other tasks and will eventually be merged
    # into the result list and returned together.
    results = await asyncio.gather(
        *aws, return_exceptions=True
    )  # need to unpack the list
    # results = await asyncio.gather(*aws, return_exceptions=False)  # need to unpack the list
    for result in results:
        print(f">got : {result}")


# adding a new task in the group
async def main():
    aws, results = [], []
    for i in range(3):
        aws.append(asyncio.create_task(some_coro(f"name-{i}")))
    group_1 = asyncio.gather(*aws)  # note we don't use await now
    # when some situation happen, we may add a new task
    group_2 = asyncio.gather(group_1, asyncio.create_task(some_coro("a new task")))
    results = await group_2
    for result in results:
        print(f">got : {result}")


# adding a timeout
async def main():
    aws, results = [], []
    for i in range(3):
        aws.append(asyncio.create_task(some_coro(f"name-{i}")))

    results = await asyncio.wait_for(asyncio.gather(*aws), timeout=2)
    for result in results:
        print(f">got : {result}")


async def main():
    aws = []
    for i in range(5):
        aws.append(asyncio.create_task(some_coro(f"name-{i}")))

    for done in asyncio.as_completed(aws):  # we don't need to unpack the list
        try:
            result = await done
            print(f">got : {result}")
        except AsyncException as e:
            print(e)


async def main():
    aws = set()
    for i in range(5):
        aws.add(asyncio.create_task(some_coro(f"name-{i}")))

    done, pending = await asyncio.wait(aws, return_when=asyncio.FIRST_COMPLETED)
    for task in done:
        try:
            result = await task
            print(f">got : {result}")
        except AsyncException as e:
            print(e)
    print(f"the length of pending is {len(pending)}")


asyncio.run(main())
