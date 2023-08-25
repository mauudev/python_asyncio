#
## example of asyncio task group with a canceled task
#
import asyncio


async def task1():
    await asyncio.sleep(1)
    print("Hello from coroutine 1")


async def task2():
    await asyncio.sleep(1)
    print("Hello from coroutine 2")


async def task3():
    await asyncio.sleep(1)
    print("Hello from coroutine 2")


async def main():
    async with asyncio.TaskGroup() as group:
        t1 = group.create_task(task1())
        t2 = group.create_task(task2())
        t3 = group.create_task(task3())
        await asyncio.sleep(0.5)
        t2.cancel()

    print(f"Task1: done={t1.done()}, cancelled={t1.cancelled()}")
    print(f"Task2: done={t2.done()}, cancelled={t2.cancelled()}")
    print(f"Task3: done={t3.done()}, cancelled={t3.cancelled()}")


asyncio.run(main())
